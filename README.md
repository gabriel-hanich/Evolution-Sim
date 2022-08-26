# Evolution-Sim
Simulating Natural selection through a population of predators and prey

Note - The frequency distribution between the mean and the variation is given by a Gaussian distribution

# Meaning of Setup Parameters 

## Sim
- `length` - The number of 'turns' the sim has
- `breedTurns` - After how many turns the animals breed 

## Board
- `boardSizeX` - The width of the board the animals inhabit
- `boardSizeY` - The height of the board

## Food
- `foodCount` - The number of food sources that spawn
- `meanEnergy` - The mean amount of energy provided by a food sources
- `energyVariation` - The variation of amount of energy provided
- `spawnThreshold` - The number multiplied by the total population to get when the food sources need replenishing

## Prey
Both health and energy are values between 0 and 1, with 1 being full and 0 being empty (duh)
- `preyCount` - The number of prey that spawn at the start
- `meanSpeed` - The mean of the speed value a prey will have
- `speedVariation` - How much the speed value will be varied
- `meanSensingRange` - The mean range an animal can sense (see)
- `sensingRangeVariation` - The variation of the sensing range

## Predators
- `predatorCount` The number of predators that spawn at the start

# Formula for traits
## Prey
- Efficiency = log(speed + 1) / 15
- Energy Cost from movement = distance * (3 - Efficiency)

# Outputted .csv file format
| Column Letter | Column A | Coulumn B| Column C | Column D |
|---|---|---|---|---| 
| Description | Turn Number | Total Prey Population | Average Energy | Number of new prey born THAT turn
