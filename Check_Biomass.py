import math

import cobra
from mewpy.simulation import get_simulator

if __name__ == '__main__':

    model = model = cobra.io.read_sbml_model(r'C:/Users/andre/OneDrive/Ambiente de Trabalho/ElectricAlgae/Model_Photoautotrophy.xml')
    envcond = {'EX_photonVis_LPAREN_e_RPAREN_' : (-200.0, 0.0),
               "EX_ncam_LPAREN_e_RPAREN_": (-1000, 0 ),
               "EX_thm_LPAREN_e_RPAREN_": (-1000, 0),
               "EX_btn_LPAREN_e_RPAREN_": (-1000, 0),
               "EX_h2o_LPAREN_e_RPAREN_": (-1000, 1000),
               "DM_o2D_LPAREN_u_RPAREN_": (-1000, 1000),
               "EX_h_LPAREN_e_RPAREN_": (-1000, 1000),
               "EX_co2_LPAREN_e_RPAREN_": (-20, 0),
               'PRISM_incandescent_60W' : (-1000.0,1000.0), 'PRISM_solar_litho' : (0.0,0.0), 'PRISM_solar_exo' : (0.0,0.0),
                'PRISM_fluorescent_warm_18W' : (0.0,0.0), 'PRISM_fluorescent_cool_215W' : (0.0,0.0), 'PRISM_metal_halide' : (0.0,0.0),'PRISM_high_pressure_sodium' : (0.0,0.0),
                'PRISM_growth_room' : (0.0,0.0), 'PRISM_white_LED' : (0.0,0.0), 'PRISM_red_LED_array_653nm' : (0.0,0.0), 'PRISM_red_LED_674nm' : (0.0,0.0), 'PRISM_design_growth' : (0.0,0.0)}
    
    simul = get_simulator(model, envcond=envcond)
    result = simul.simulate(method='pFBA')
    print(result.fluxes["Biomass_Cvu_auto_DASH_"])

    car = {"dcaro_h" : {'ASPSE': (0, 0.0), 'GLYK': (0, 0.0002587514776586086), 'PSAT': (0, 0), 'SGAT': (0, 0), 'SPTA': (0, 0), 'PGDH': (0, 0), 'PGDHh': (0, 0), 'CS': (0, 0), 'CSm': (0, 0), 'CSx': (0, 0)},
           'acaro_h' : {'ASPO': (0, 0.0), 'ASPOm': (0, 0.0), 'PGLYCPh': (0, 0.0), 'G6PI': (0, 0.0), 'G6PIh': (0, 0.0), 'PGIA': (0, 0.0), 'PGIAh': (-0.7281588690377873, 0), 'PGIB': (0, 0.0), 'PGIBh': (0, 0.0), 'CYOO6m': (0, 0.031864310600408716), 'CYOR_LPAREN_q8_RPAREN_m': (0, 0.018893360725818667), 'LLDH_LPAREN_ferr_RPAREN_m': (0, 0.0), 'LLDH_LPAREN_ferr_RPAREN_x': (0, 0.0), 'gorCv': (0, 0.0)},
           'crpxan_u' : {'BCAROKT': (0, 0.0), 'GLYK': (0, 0.0005175029553180866), 'G6PI': (0, 0.0), 'G6PIh': (0, 0.0), 'PGIA': (-0.03397077712662936, 0), 'PGIAh': (-0.6941070383622687, 0), 'PGIB': (-3.4511617714036696e-05, 0), 'PGIBh': (0, 0.0), 'DOLASNT': (0, 0), 'GLCNACT': (0, 0), 'CEF': (0, 0.8325755866503739)},
           'lut_u' : {'GDHm': (0, 0.0), 'GDH': (0, 0.0), 'GDH_LPAREN_nadp_RPAREN_': (0, 0.0), 'PSAT': (0, 0), 'SGAT': (0, 0), 'SPTA': (0, 0), 'G6PI': (0, 0.0), 'G6PIh': (0, 0.0), 'PGIA': (0, 0.0), 'PGIAh': (-0.7282286930918564, 0), 'PGIB': (0, 0.0), 'PGIBh': (0, 0.0), 'BDMT': (0, 0.0), 'G6PADH': (0, 0.0), 'G6PBDH': (0, 0.0), 'HIUH': (0, 0.0)},
           'caro_u' : {'GLYK': (0, 0), 'PGIA': (0, 0.0), 'PGIAh': (-0.7282426595103733, 0), 'PGIB': (0, 0.0), 'PGIBh': (0, 0.0), 'GLCNACPT': (0, 0.0), 'G6PADH': (0, 0.0), 'G6PBDH': (0, 0.0)},
           'vioxan_u' : {'GLYC3Pth': (0, 0.0017856970497476567), 'PSAT': (0, 0), 'SGAT': (0, 0), 'SPTA': (0, 0), 'PGDH': (0, 0.0), 'PGDHh': (0, 0.0)}}
    
    
    for caroteno in car.keys():
        const = car[caroteno]
        copy = model.copy()
        simulator = get_simulator(copy, envcond=envcond, constraints=const)
        copy.add_boundary(copy.metabolites.get_by_id(caroteno), type="demand")
        sol = simulator.simulate(method='FBA')
        print(caroteno)
        print(sol.fluxes["Biomass_Cvu_auto_DASH_"])