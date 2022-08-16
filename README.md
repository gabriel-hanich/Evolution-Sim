# Evolution-Sim
Simulating Natural selection through a population of predators and prey

Note - The frequency distribution between the mean and the variation is given by a Gaussian distribution

# Meaning of Setup Parameters 
## Board
- `boardSizeX` - The width of the board the animals inhabit
- `boardSizeY` - The height of the board

## Prey
- `preyCount` - The number of prey that spawn at the start
- `meanMaxHealth` - The mean max health an animal will have
- `maxHealthVariation` - The maximum amount of variation of maximum health prey will have
- `meanSpeed` - The mean of the speed value a prey will have
- `speedVariation` - How much the speed value will be varied
- `meanMaxEnergy` - The mean max energy a prey will have
- `maxEnergyVariation` - The variation of max energy values
- `meanSensingRange` - The mean range an animal can sense (see)
- `sensingRangeVariation` - The variation of the sensing range

## Predators
- `predatorCount` The number of predators that spawn at the start

# Formula for traits
## Prey
- Efficiency = log(speed / 3) + 1
