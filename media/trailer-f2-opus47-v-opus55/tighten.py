import numpy as np, subprocess, glob, os, sys, json
FF="/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
SR=44100
MAXGAP=float(sys.argv[1]) if len(sys.argv)>1 else 0.25
THR=float(sys.argv[2]) if len(sys.argv)>2 else -42
os.makedirs('tight',exist_ok=True)
durs={}
for f in sorted(glob.glob('audio2/*.mp3')):
    b=os.path.basename(f)[:-4]
    raw=subprocess.run([FF,'-loglevel','error','-i',f,'-af','atempo=1.06,loudnorm=I=-16:TP=-1.5:LRA=11','-ar',str(SR),'-ac','1','-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32).copy()
    win=int(0.02*SR); n=len(x)//win
    rms=np.sqrt((x[:n*win].reshape(n,win)**2).mean(1)+1e-12)
    db=20*np.log10(rms); loud=db>THR
    idx=np.where(loud)[0]
    first,last=idx[0],idx[-1]
    keep=[]; i=first; 
    segs=[]
    # build list of frames to keep: shrink quiet runs longer than MAXGAP
    run=[]
    out=[]
    for k in range(first,last+1):
        if loud[k]:
            if run:
                L=len(run)
                if L*0.02>MAXGAP:
                    h=int(MAXGAP/0.02/2); run=run[:h]+run[-h:]
                out+=run; run=[]
            out.append(k)
        else: run.append(k)
    y=np.concatenate([x[k*win:(k+1)*win] for k in out])
    pad=np.zeros(int(0.06*SR),dtype=np.float32)
    y=np.concatenate([pad,y,pad*2])
    # short fades
    fl=int(0.01*SR); y[:fl]*=np.linspace(0,1,fl); y[-fl:]*=np.linspace(1,0,fl)
    y.astype(np.float32).tofile(f'tight/{b}.f32')
    durs[b]=len(y)/SR
    print(b, round(len(x)/SR,2),'->',round(len(y)/SR,2))
json.dump(durs,open('tight/durs.json','w'),indent=1)
print('total',round(sum(durs.values()),2))
