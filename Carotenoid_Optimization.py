import math

import cobra
from mewpy.simulation import get_simulator
#from reframed.io.sbml import load_cbmodel
from mewpy.optimization.evaluation import BPCY, WYIELD, BPCY_FVA
from mewpy.problems import GKOProblem, GOUProblem
from mewpy.optimization import EA
from mewpy.util.utilities import population_to_csv


if __name__ == '__main__':
    model = cobra.io.read_sbml_model(r'C:/Users/andre/OneDrive/Ambiente de Trabalho/ElectricAlgae/Models/Model_Photoautotrophy.xml')
    biomass_reaction = "Biomass_Cvu_auto_DASH_"
    # environmental conditions
    envcond = {
            #'EX_photonVis_LPAREN_e_RPAREN_': (-2000.0, 1000),
               "EX_ncam_LPAREN_e_RPAREN_": (-1000, 1000),
               "EX_thm_LPAREN_e_RPAREN_": (-1000, 1000),
               "EX_btn_LPAREN_e_RPAREN_": (-1000, 1000),
               "EX_h2o_LPAREN_e_RPAREN_": (-1000, 1000),
               "DM_o2D_LPAREN_u_RPAREN_": (-1000, 1000),
               "EX_h_LPAREN_e_RPAREN_": (-1000, 1000),
               "EX_co2_LPAREN_e_RPAREN_": (-20, 1000),
               'PRISM_incandescent_60W': (-1000.0, 1000.0), 'PRISM_solar_litho': (0.0, 0.0), 'PRISM_solar_exo': (0.0, 0.0),
               'PRISM_fluorescent_warm_18W': (0.0, 0.0), 'PRISM_fluorescent_cool_215W': (0.0, 0.0), 'PRISM_metal_halide': (0.0, 0.0), 'PRISM_high_pressure_sodium': (0.0, 0.0),
               'PRISM_growth_room': (0.0, 0.0), 'PRISM_white_LED': (0.0, 0.0), 'PRISM_red_LED_array_653nm': (0.0, 0.0), 'PRISM_red_LED_674nm': (0.0, 0.0),
               'PRISM_design_growth': (0.0, 0.0)}


    simulator = get_simulator(model, envcond=envcond)
    simulator.set_objective(biomass_reaction)
    essential_genes = simulator.essential_genes

    carotenoids = ["anxan_u", "acaro_h", "acaro_u", "caro_u", "bcrptxan_u", "crpxan_u", "dcaro_h", "ecaro_h", "gcaro_h" , "gcaro_u" , "lut_u" , "neoxan_u" , "norsp_h" ,
                    "phyto_h", "vioxan_u", "vioxan_c", "9cvioxan_c", "vioxan_h", "zxan_u", "zcaro_h", "zaxan_u"]
    
    for carotenoid in carotenoids:
        try:
            model.add_boundary(model.metabolites.get_by_id(carotenoid), type="demand")
        except Exception as e:
            print(e)
        try:
            model.reactions.Biomass_Cvu_auto_DASH_.add_metabolites({carotenoid: -model.reactions.Biomass_Cvu_auto_DASH_.metabolites[model.metabolites.get_by_id(carotenoid)]})
            print(model.metabolites.get_by_id(carotenoid) in model.reactions.Biomass_Cvu_auto_DASH_.metabolites.keys())
        except Exception as e:
            print(e)
    
    for carotenoid in carotenoids:
         try:
             demand_id = "DM_" + carotenoid
             evaluator_1 = BPCY_FVA(biomass_reaction, demand_id, method='pFBA')#, uptake="EX_co2_LPAREN_e_RPAREN_"
             evaluator_2 = WYIELD(biomass_reaction, demand_id, min_biomass_per= 0.3, scale=True)
             problem = GKOProblem(model, fevaluation=[evaluator_1, evaluator_2], envcond=envcond, non_target=essential_genes)
             ea = EA(problem, max_generations=20)
             final_pop = ea.run()
             population_to_csv(problem, final_pop, 'GKO_pFBA_' + carotenoid + '.csv')
         except Exception as e:
             print(e)

    for carotenoid in carotenoids:
        try:
            demand_id = "DM_" + carotenoid
            evaluator_1 = BPCY_FVA(biomass_reaction, demand_id, method='pFBA') # uptake="EX_co2_LPAREN_e_RPAREN_",
            evaluator_2 = WYIELD(biomass_reaction, demand_id, min_biomass_per= 0.3, scale=True)
            problem = GOUProblem(model, fevaluation=[evaluator_1, evaluator_2], envcond=envcond, non_target=essential_genes, levels = [0,1/2,1/4,1/16,1/32] )
            ea = EA(problem, max_generations=30)
            final_pop = ea.run()
            population_to_csv(problem, final_pop, 'GOU_pFBA_v3' + carotenoid + '.csv')
        except Exception as e:
            print(e)
