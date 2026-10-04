import numpy as np, json, subprocess
SR=44100
S=json.load(open('schedule.json')); T=S['total']; N=int(T*SR)+SR
speech=np.zeros(N,np.float32)
for k,v in S.items():
    if k=='total': continue
    x=np.fromfile(f'tight/{k}.f32',dtype=np.float32)
    i=int(v['start']*SR) - int(0.06*SR)  # pad compensation
    i=max(i,0); speech[i:i+len(x)]+=x
t=np.arange(N)/SR
rng=np.random.default_rng(7)
def lp(x,a):  # one-pole lowpass
    y=np.empty_like(x); acc=0.0
    # vectorized via scipy-less filter: use cumulative approach in chunks
    from numpy import frompyfunc
    return _lp(x,a)
def _lp(x,a):
    import numpy as np
    y=np.zeros_like(x); 
    b=1-a
    # IIR via loop in chunks (fast enough for ~3M samples? use lfilter-like recursion with numpy cumsum trick not exact) 
    acc=0.0
    for i in range(0,len(x)):
        acc=a*acc+b*x[i]; y[i]=acc
    return y
# drone
lfo=0.6+0.4*np.sin(2*np.pi*0.07*t)
drone=(0.5*np.sin(2*np.pi*55*t)+0.35*np.sin(2*np.pi*82.41*t+1)+0.18*np.sin(2*np.pi*110.3*t+2)+0.08*np.sin(2*np.pi*164.8*t))*lfo
# dark wind: smoothed noise via FFT lowpass
n=rng.standard_normal(N).astype(np.float32)
F=np.fft.rfft(n); f=np.fft.rfftfreq(N,1/SR); F*=1/(1+(f/250)**4); wind=np.fft.irfft(F,N)
wind/=np.abs(wind).max(); wind*=0.5*(0.6+0.4*np.sin(2*np.pi*0.05*t+1))
bed=(drone*0.6+wind*0.5).astype(np.float32)
# envelope: fade in/out, swell on night scene, cut on closing tail
env=np.clip(t/2.0,0,1)*np.clip((T-t)/2.0,0,1)
bed*=env*0.09
# events
ev=np.zeros(N,np.float32)
def add(at,sig,g):
    i=int(at*SR); j=min(N,i+len(sig)); ev[i:j]+=g*sig[:j-i]
def tick(dur=0.05,f0=2400):
    tt=np.arange(int(dur*SR))/SR
    return (np.sin(2*np.pi*f0*tt)*np.exp(-tt*120)+0.5*rng.standard_normal(len(tt))*np.exp(-tt*300)).astype(np.float32)
def knock():
    tt=np.arange(int(0.25*SR))/SR
    return (np.sin(2*np.pi*180*tt)*np.exp(-tt*25)+0.3*np.sin(2*np.pi*420*tt)*np.exp(-tt*40)).astype(np.float32)
def boom(dur=2.5,f0=60):
    tt=np.arange(int(dur*SR))/SR
    fr=f0*(1+1.5*np.exp(-tt*12)); ph=2*np.pi*np.cumsum(fr)/SR
    nz=rng.standard_normal(len(tt)); Fz=np.fft.rfft(nz); fz=np.fft.rfftfreq(len(tt),1/SR); Fz*=1/(1+(fz/400)**2); nz=np.fft.irfft(Fz,len(tt)); nz/=np.abs(nz).max()
    return (np.sin(ph)*np.exp(-tt*2.2)+0.35*nz*np.exp(-tt*8)).astype(np.float32)
def bell(f=196,dur=6.0):
    tt=np.arange(int(dur*SR))/SR
    parts=[(0.5,1.0,0.9),(1.0,0.8,1.3),(1.19,0.5,1.8),(1.56,0.35,2.4),(2.0,0.3,2.8),(2.51,0.2,3.5),(3.0,0.12,4.5),(4.07,0.08,6)]
    y=sum(a*np.sin(2*np.pi*f*r*tt+r)*np.exp(-tt*d*0.6) for r,a,d in parts)
    y*=np.clip(tt/0.004,0,1)
    return (y/np.abs(y).max()).astype(np.float32)
c=lambda k:S[k]
# clock ticks during setup through day 3 (soft), alternating pitch
tk=tick(); tk2=tick(f0=1900)
x=c('c03')['start']; k=0
while x < c('c15')['end']-0.6:
    add(x, tk if k%2==0 else tk2, 0.05); x+=1.0; k+=1
# title bell
add(c('c03')['start']-0.05, bell(147,6), 0.16)
# Casey executed
add(c('c07')['start']+1.6, boom(), 0.32)
# Jules executed & Blair becomes Imp
add(c('c11')['start']+0.1, boom(2.5,55), 0.32)
add(c('c11')['start']+1.4, bell(110,4), 0.10)
# nomination
add(c('c14')['start'], boom(1.5,70), 0.18)
# vote knocks
ts=c('c15')['end']-0.35; te=c('c16')['start']-0.2
for v in range(8):
    at=(ts+0.2)+(v/8)*(te-ts-0.2)+0.001
    add(at, knock(), 0.22)
# final: big boom + bell
add(c('c16')['start']-0.15, boom(3.5,45), 0.45)
add(c('c16')['start']-0.1, bell(98,7), 0.22)
# cold open hit on "8 YES"
add(c('c02')['start']-0.1, boom(2.0,50), 0.3)
# closing soft bell
add(c('c17')['start']-0.1, bell(196,5), 0.08)
# ducking from speech envelope
e=np.abs(speech); w=int(0.05*SR); k_=np.ones(w)/w
se=np.convolve(e,k_,mode='same')
se=np.convolve((se>0.01).astype(np.float32),np.ones(int(0.3*SR))/int(0.3*SR),mode='same')
duck=1-0.55*np.clip(se,0,1)
mix=speech*1.0+bed*duck+ev*(1-0.35*np.clip(se,0,1))
mix=mix[:int(T*SR)]
pk=np.abs(mix).max(); print('peak',pk)
mix=mix/max(pk,1e-6)*0.89
mix.astype(np.float32).tofile('mix.f32')
print('dur',len(mix)/SR)
