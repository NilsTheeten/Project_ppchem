# Project_ppchem
This repository contains the ppchem project: Hydroponics
Description: Hydroponics is a type of horticulture and a subset of hydroculture which involves growing plants, usually crops or medicinal plants, without soil, by using water-based mineral nutrient solutions in an artificial environment. Terrestrial or aquatic plants may grow freely with their roots exposed to the nutritious liquid or the roots may be mechanically supported by an inert medium such as perlite, gravel, or other substrates.

Uses: More efficient way of growing crops. Researched as way of growing crops on Mars (Elon Musk) https://www.nasa.gov/science-research/nasa-plant-researchers-explore-question-of-deep-space-food-crops/

Important factors: pH --> depending on plant different pH is needed (in general 6-7) concentration of different salts (enough of some salt, not too much NaCl) solubility ( no precipitation of usefull salts) price (optimize expenses) needs of the plant quantity of salts contained in a plant

Plants: Patato Sweet patato Lettuce (Iceberg, Butterhead) soybeans

Atoms in the solution: (see Hoagland solution) N 210 ppm P 31 ppm S 64 ppm Cl 0.14 ppm / 0.65 ppm B 0.11 ppm / 0.5 ppm Na 0 ppm / 0.023 ppm / 1.2 ppm* Mg 48.6 ppm K 235 ppm Ca 200 ppm / 160 ppm Mn 0.11 ppm / 0.5 ppm Zn 0.023 ppm / 0.05 ppm Cu 0.014 ppm / 0.02 ppm Mo 0.018 ppm / 0.048 ppm / 0.011 ppm Fe 1 ppm / 5 ppm / 2.9 ppm*

Salts in the solution: Potassium nitrate, KNO3 Calcium nitrate tetrahydrate, Ca(NO3)2•4H2O Magnesium sulfate heptahydrate, MgSO4•7H2O Potassium dihydrogen phosphate, KH2PO4 or Ammonium dihydrogen phosphate, (NH4)H2PO4 Boric acid, H3BO3 Manganese chloride tetrahydrate, MnCl2•4H2O Zinc sulfate heptahydrate, ZnSO4•7H2O Copper sulfate pentahydrate, CuSO4•5H2O Molybdic acid monohydrate, H2MoO4•H2O or Sodium molybdate dihydrate, Na2MoO4•2H2O Ferric tartrate or Iron(III)-EDTA− or Iron chelate (Fe-EDDHA−)

Idea: Provide tools to help manage hydroponic plantations

Quantity of salts to add, when
Where to buy the salt (cheapest price)
Regulate the pH of the solution
Bonus: provide security indications
Implementation/useful tools:

Modelisations of salt concentrations/pH (needs to be 6-7, depends on plant) over time
Recommend salts to add/quantity/seller given a plant an the mixture of salts in the solution
Define optimal composition
Difine loss of salts depending on plant growth
Depending on number/type of plant, how much solution must be added
Volume is constant (automatic refilling of bassin with distilled water)
Modelise buffer solution
Modelisation: We have a closed system where plants can grow using water und salts, after time t=growth_time they are replaced by a new baby plant

Define constant volume of water in the tank [L] and constant T (298K)
Define optimal concentration of the different salts (Hoagland)
Choose plant --> return how much salt to add when, figures of salt concentration over time, ...
