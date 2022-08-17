# Evolution-Sim
Simulating Natural selection through a population of predators and prey

Note - The frequency distribution between the mean and the variation is given by a Gaussian distribution

# Meaning of Setup Parameters 

## Sim
- `length` - The number of 'turns' the sim has

## Board
- `boardSizeX` - The width of the board the animals inhabit
- `boardSizeY` - The height of the board

## Food
- `foodCount` - The number of food sources that spawn
- `meanEnergy` - The mean amount of energy provided by a food sources
- `energyVariation` - The variation of amount of energy provided

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
