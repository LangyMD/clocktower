# Game flow, step by step

A summary in our own words of the standard procedure, written so that each step maps onto something an engine
has to implement. Official sources: [Rules Explanation](https://wiki.bloodontheclocktower.com/Rules_Explanation),
[Setup](https://wiki.bloodontheclocktower.com/Setup), [Nominations and voting](https://wiki.bloodontheclocktower.com/Rules_Explanation#Nominations).

## 1. Setup (before night 1)

1. **Pick a script** and seat the players in a circle. Seating order matters: many abilities refer to
   neighbours, and votes go clockwise.
2. **Look up the counts** of Townsfolk, Outsiders, Minions and Demons for the number of (non-Traveller) players
   ([setup-counts.json](../data/setup-counts.json)).
3. **Choose characters**: the Storyteller picks that many of each type from the script. Characters with a
   bracketed **setup modifier** change the counts (the Baron adds two Outsiders and removes two Townsfolk, for
   example). Some characters are never put in the bag (the Drunk, the Marionette); the Storyteller swaps in a
   different token and notes the truth in the Grimoire.
4. **Deal** the tokens at random. Each player secretly learns their character (a Drunk sees a Townsfolk token).
5. **Prepare the Grimoire**: the Storyteller's board with every player's real character, plus reminder tokens.
   Choose any setup-time secrets: the Fortune Teller's **red herring**, what the Drunk believes, the Demon's
   three bluffs.
6. **Travellers** may join (or leave) at almost any time; their alignment is chosen by the Storyteller and they
   are publicly known to be Travellers. **Fabled** and **Loric** are announced if used.

## 2. The first night

The Storyteller wakes characters one at a time in the script's **first-night order**
([night-order.json](../data/night-order.json); the markers `dusk`, `minioninfo`, `demoninfo` and `dawn` are
steps, not characters). In 7+ player games:

- **Minion info**: the Minions wake together and learn who the Demon is (and see each other).
- **Demon info**: the Demon learns who its Minions are and is shown three good characters not in play (bluffs).
- Characters with a first-night ability then act or receive information in order.

In 5 and 6 player games the evil team does not get this information and the Demon gets no bluffs. Characters
marked with a `*` in their ability (night `*`) do not act on the first night; in the data they have
`first_night: null`.

## 3. Day

1. **Dawn**: the Storyteller announces who died in the night (never how or why).
2. **Discussion**: players talk openly and in private, in any combination. Anyone may say anything, true or
   false; there is no rule against lying, showing a character token is not allowed, and secrets are only as
   safe as the person you told.
3. **Day abilities** (Slayer, Gossip, Savant, Artist, Juggler and others) are used when their text allows, often
   in public.
4. **Nominations** open when the Storyteller calls for them.

## 4. Nominations, voting and execution

- **Who may nominate**: each *living* player may nominate once per day; each player may be nominated once per day.
  Dead players cannot nominate.
- **Defence and accusation**: the nominator may say why; the nominee may respond. The Storyteller limits time.
- **Voting**: the Storyteller moves a hand clockwise around the circle, starting with the player after the
  nominee and ending with the nominee. Each player votes by having their hand raised when the hand reaches them.
  Living players may vote on every nomination. A dead player may vote **only once for the rest of the game**
  (they spend their ghost vote token).
- **Threshold**: a nomination is "on the block" if its votes are **at least half the living players** (rounded
  up), and more than any earlier nomination that day. If a later nomination **ties** the leader, *neither* is on
  the block (unless a later nomination beats both).
- **Execution**: at the end of the day, whoever is on the block is executed. At most one execution per day. Some
  abilities execute immediately (the Virgin). An executed player usually dies, but not always (Pacifist,
  Devil's Advocate, Fool, Zombuul, Vizier). "Execution" and "death" are different things to the rules.
- **Exile**: Travellers are not executed; anyone may call for a Traveller's exile, it uses all players' votes
  (dead and alive, no ghost token needed), the threshold is half of all players, and it does not count as the
  day's execution.

## 5. Later nights

1. Dusk: the Storyteller tells everyone to close their eyes.
2. Characters wake in the **other-nights order**. Typical sequence: protection and poison first, then the
   Demon's kill, then characters that react to deaths (Ravenkeeper, Sage), then information roles so that
   their information reflects the night's events.
3. Dawn: deaths are announced.

## 6. Game end

The Storyteller checks win conditions continually:

- Good wins immediately when the Demon dies and no ability replaces it (Scarlet Woman, Imp starpass, Fang Gu
  jump, Mastermind and similar).
- Evil wins when two players live (counting only non-Travellers) and one is the Demon, and at other times defined
  by abilities (Saint executed, Evil Twin's good twin executed, Vortox with no execution, Leviathan on day 6 or
  after two good executions, and so on).
- Players who have died stay on their team and win or lose with it.

At the end the Storyteller reveals the Grimoire and usually walks the table through what happened. This
post-game explanation is a big part of why players enjoy the game, and an AI Storyteller should produce one.

## Timing notes the engine must get right

- **"Tonight" and "tomorrow"**: a poison chosen tonight lasts until dusk tomorrow; a drunkenness "until dusk"
  ends at the start of the next night.
- **Deaths at night are simultaneous for announcing purposes**, but abilities resolve in night order, so a
  player killed before their turn in the order does not wake (unless the ability triggers on death).
- **A dead player's ability stops working** unless the text says otherwise ("even if dead", "even if you die").
- **Information reflects the moment the character wakes**, so a Chambermaid or Mathematician late in the order
  sees more of the night than one early in the order.
