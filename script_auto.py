import os
import shutil
import time
import pandas as pd



def gml_creator(n, bottom_depth):
    script = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<?xml-stylesheet type="text/xsl" href="OpenGeoSysGLI.xsl"?>

<OpenGeoSysGLI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.opengeosys.org/images/xsd/OpenGeoSysGLI.xsd" xmlns:ogs="http://www.opengeosys.org">
    <name>beier_sandbox</name>
    <points>
        <point id="0" x="0.0" y="20.0" z="-{}" name="BHE_BOTTOM"/>
        <point id="1" x="0.0" y="20.0" z="0" name="BHE_TOP"/>
    </points>
    <polylines>
        <polyline id="0" name="BHE_1">
            <pnt>1</pnt>
            <pnt>0</pnt>
        </polyline>
    </polylines>
</OpenGeoSysGLI>'''.format(bottom_depth)
                
    f = open("3D_deep_BHE_{}.gml".format(n), "w")
    f.write(script)
    f.close()

    gml_file_name = "3D_deep_BHE_{}".format(n)
    return gml_file_name

def geo_creator(n, bottom_depth):
    script = '''// Gmsh project created on Thu Nov 04 10:01:46 2021
SetFactory("OpenCASCADE");

Point(1) = {20, 40, 0, 40};
Point(2) = {-20, 40, 0, 40};
Point(3) = {-20, 0, 0, 40};
Point(4) = {20, 0, 0, 40};
Point(5) = {0, 20, 0, 0.2};

Point(6) = {0, 20, 0, 1};
Point(7) = {0, 20, -%s, 1};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {6, 7};

Curve Loop(1) = {2, 3, 4, 1};
Plane Surface(1) = {1};
Point{5} In Surface{1};

Extrude {0, 0, -%s} {
  Surface{1}; Layers {%s}; Recombine;
}
Transfinite Curve {3, 2, 1, 4} = 6 Using Progression 1;



Line{5} In Volume{1};

Physical Curve("BHE_1", 1) = {5};
Physical Volume("BHE_soil", 2) = {1};''' % (bottom_depth,bottom_depth,bottom_depth)

    f = open("3D_deep_BHE_{}.geo".format(n), "w")
    f.write(script)
    f.close()
    
    geo_file_name = "3D_deep_BHE_{}".format(n)
    return geo_file_name
    
def msh_to_vtu(geo_file):
    os.system('cmd /c "GMSH2OGS -i {}.msh -o {}.vtu"'.format(geo_file, geo_file))
    

def folder_creator(no):
    # Directory
    directory = "Sample_%s" % no

    # Parent Directory path
    parent_dir = r"D:\YasinAhmadpoor\thesis\automation"

    # Path
    path = os.path.join(parent_dir, directory)    
    
    os.mkdir(path)
    print("Directory '% s' created" % directory)
    
    return path

def prj_creator(vtu_file,gml_file,flow_rate,depth,diameter,outer_diameter,outer_thickness,
                inner_diameter,inner_thickness,
                inner_wall_thermal_conductivity,fluid_density,
                fluid_viscosity,fluid_specific_heat_capacity,fluid_thermal_conductivity,
                formation_specific_heat_capacity,formation_density,formation_thermal_conductivity,
                geothermal_gradient,inlet_temperature, n):
    script = ''' <?xml version="1.0" encoding="ISO-8859-1"?>
<OpenGeoSysProject>
    <mesh>{0}.vtu</mesh>
    <geometry>{1}.gml</geometry>
    <processes>
        <process>
            <name>HeatTransportBHE</name>
            <type>HEAT_TRANSPORT_BHE</type>
            <integration_order>2</integration_order>
            <process_variables>
                <process_variable>temperature_soil</process_variable>
                <process_variable>temperature_BHE1</process_variable>
            </process_variables>
            <borehole_heat_exchangers>
                <borehole_heat_exchanger>
                    <type>CXA</type>
                    <flow_and_temperature_control>
                        <type>TemperatureCurveConstantFlow</type>
                        <flow_rate>{2}</flow_rate>
                        <temperature_curve>inflow_temperature</temperature_curve>
                    </flow_and_temperature_control>
                    <borehole>
                        <length>{3}</length>
                        <diameter>{4}</diameter>
                    </borehole>
                    <grout>
                        <density>2010</density>  
                        <porosity>0.0</porosity>
                        <specific_heat_capacity>736</specific_heat_capacity>
                        <thermal_conductivity>0.53</thermal_conductivity>
                    </grout>
                    <pipes>
                        <outer>
                            <diameter> {5}</diameter> 
                            <wall_thickness>{6}</wall_thickness>
                            <wall_thermal_conductivity>45</wall_thermal_conductivity>
                        </outer>
                        <inner>
                            <diameter>{7}</diameter>  
                            <wall_thickness>{8}</wall_thickness>
                            <wall_thermal_conductivity>{9}</wall_thermal_conductivity>
                        </inner>
                        <longitudinal_dispersion_length>0.001</longitudinal_dispersion_length>
                    </pipes>
                    <refrigerant>
                        <density>{10}</density>  
                        <viscosity>{11}</viscosity>
                        <specific_heat_capacity>{12}</specific_heat_capacity>
                        <thermal_conductivity>{13}</thermal_conductivity>
                        <reference_temperature>288.15</reference_temperature>
                    </refrigerant>
                </borehole_heat_exchanger>
            </borehole_heat_exchangers>
        </process>
    </processes>
    <media>
        <medium id="0">
            <phases>
                <phase>
                    <type>AqueousLiquid</type>
                    <properties>
                        <property>
                            <name>phase_velocity</name>
                            <type>Constant</type>
                            <value>0 0 0</value>
                        </property>
                        <property>
                            <name>specific_heat_capacity</name>
                            <type>Constant</type>
                            <value>4068</value>
                        </property>
                        <property>
                            <name>density</name>
                            <type>Constant</type>
                            <value>992.92</value>
                        </property>
                    </properties>
                </phase>
                <phase>
                    <type>Solid</type>
                    <properties>
                        <property>
                            <name>specific_heat_capacity</name>
                            <type>Constant</type>
                            <value>{14}</value>
                        </property>
                        <property>
                            <name>density</name>
                            <type>Constant</type>
                            <value>{15}</value>
                        </property>
                    </properties>
                </phase>
                <phase>
                    <type>Gas</type>
                    <properties>
                        <property>
                            <name>specific_heat_capacity</name>
                            <type>Constant</type>
                            <value>1000</value>
                        </property>
                        <property>
                            <name>density</name>
                            <type>Constant</type>
                            <value>2500</value>
                        </property>
                    </properties>
                </phase>
            </phases>
            <properties>
                <property>
                    <name>porosity</name>
                    <type>Constant</type>
                    <value>0</value>
                </property>
                <property>
                    <name>thermal_conductivity</name>
                    <type>Constant</type>
                    <value>{16}</value>
                </property>
                <property>
                    <name>thermal_longitudinal_dispersivity</name>
                    <type>Constant</type>
                    <value>0</value>
                </property>
                <property>
                    <name>thermal_transversal_dispersivity</name>
                    <type>Constant</type>
                    <value>0</value>
                </property>
            </properties>
        </medium>
    </media>
    <time_loop>
        <processes>
            <process ref="HeatTransportBHE">
                <nonlinear_solver>basic_picard</nonlinear_solver>
                <convergence_criterion>
                    <type>DeltaX</type>
                    <norm_type>NORM2</norm_type>
                    <reltol>1e-5</reltol>
                </convergence_criterion>
                <time_discretization>
                    <type>BackwardEuler</type>
                </time_discretization>
                <time_stepping>
                    <type>FixedTimeStepping</type>
                    <t_initial> 0.0 </t_initial>
                    <t_end> 8640000 </t_end>
                    <timesteps>
                        <pair>
                            <repeat>100</repeat>
                            <delta_t>86400</delta_t>
                        </pair>
                    </timesteps>
                </time_stepping>
            </process>
        </processes>
        <output>
            <type>VTK</type>
            <prefix>3D_deep_BHE_CXA</prefix>
            <timesteps>
                <pair>
                    <repeat> 1</repeat>
                    <each_steps> 1 </each_steps>
                </pair>
            </timesteps>
            <variables>
                <variable>temperature_soil</variable>
                <variable>temperature_BHE1</variable>
            </variables>
            <suffix>_ts_{{:timestep}}_t_{{:time}}</suffix>
        </output>
    </time_loop>
    <parameters>
        <parameter>
            <name>T0</name>
            <type>Function</type>
            <expression>-{17}*z+293</expression>
        </parameter>
        <parameter>
            <name>T0_BHE1</name>
            <type>Constant</type>
            <values>293 293 293</values>
        </parameter>
    </parameters>
    <process_variables>
        <process_variable>
            <name>temperature_soil</name>
            <components>1</components>
            <order>1</order>
            <initial_condition>T0</initial_condition>
            <boundary_conditions>
            </boundary_conditions>
        </process_variable>
        <process_variable>
            <name>temperature_BHE1</name>
            <components>3</components>
            <order>1</order>
            <initial_condition>T0_BHE1</initial_condition>
        </process_variable>
    </process_variables>
    <nonlinear_solvers>
        <nonlinear_solver>
            <name>basic_picard</name>
            <type>Picard</type>
            <max_iter>200</max_iter>
            <linear_solver>general_linear_solver</linear_solver>
        </nonlinear_solver>
    </nonlinear_solvers>
    <linear_solvers>
        <linear_solver>
            <name>general_linear_solver</name>
            <lis>-i cg -p jacobi -tol 1e-16 -maxiter 10000</lis>
            <eigen>
                <solver_type>BiCGSTAB</solver_type>
                <precon_type>ILUT</precon_type>
                <max_iteration_step>1000</max_iteration_step>
                <error_tolerance>1e-16</error_tolerance>
            </eigen>
            <petsc>
                <prefix>gw</prefix>
                <parameters>-gw_ksp_type cg -gw_pc_type bjacobi -gw_ksp_rtol 1e-16 -gw_ksp_max_it 10000</parameters>
            </petsc>
        </linear_solver>
    </linear_solvers>
    <curves>
        <curve>
            <name>inflow_temperature</name>
            <coords>0  8640000
            </coords>
            <values>{18}  {18}
            </values>
        </curve>
    </curves>

</OpenGeoSysProject>
'''.format(vtu_file,gml_file,flow_rate,depth,diameter,outer_diameter,outer_thickness,
           inner_diameter,inner_thickness,
            inner_wall_thermal_conductivity,fluid_density,
            fluid_viscosity,fluid_specific_heat_capacity,fluid_thermal_conductivity,
            formation_specific_heat_capacity,formation_density,formation_thermal_conductivity,
            geothermal_gradient,inlet_temperature)

    f = open("3D_deep_BHE_{}.prj".format(n), "w")
    f.write(script)
    f.close()
    prj_file_name = "3D_deep_BHE_{}".format(n)
    
    return prj_file_name

    
if __name__ == '__main__':
    dataset = pd.read_csv(r'D:\YasinAhmadpoor\thesis\automation\Dataset_SenAna.csv')
    n = 1
    for index, row in dataset.iterrows():
        path = folder_creator(n)
        original_ogs = r'D:\YasinAhmadpoor\thesis\automation\ogs.exe'
        original_python37 = r'D:\YasinAhmadpoor\thesis\automation\python37.dll'
        original_GMSH2OGS = r'D:\YasinAhmadpoor\thesis\automation\GMSH2OGS.exe'
        original_gmsh = r'D:\YasinAhmadpoor\thesis\automation\gmsh.exe'

        shutil.copyfile(original_ogs, path + '\ogs.exe')
        shutil.copyfile(original_python37, path + '\python37.dll')
        shutil.copyfile(original_GMSH2OGS, path + '\GMSH2OGS.exe')
        shutil.copyfile(original_gmsh, path + '\gmsh.exe')
        os.chdir(path)
        gml_file_name = gml_creator(n, row['depth'])
        geo_file_name = geo_creator(n, row['depth'])
        print(os.getcwd())
        geo_file_path = path + '\\' + geo_file_name
        geo_to_msh = 'gmsh -3 {}.geo -o {}.msh -format msh2'.format(geo_file_path,geo_file_path)
        os.system(geo_to_msh)
        msh_to_vtu(geo_file_name)
        print(geo_file_name)
        prj_file_name = prj_creator(geo_file_name,gml_file_name,row['fluid_flow_rate'],row['depth'],
                                    row['diameter'], row['outer_pipe_diameter'],
                                    row['outer_pipe_thickness'], row['inner_pipe_diameter'],
                                    row['inner_pipe_thickness'],row['inner_pipe_thermal_conductivity'],
                                    row['fluid_density'], row['fluid_viscosity'], row['fluid_specific_heat_capacity'],
                                    row['fluid_thermal_conductivity'], row['formation_specific_heat_capacity'],
                                    row['formation_density'], row['formation_thermal_conductivity'],
                                    row['geothermal_gradient'],row['inlet_fluid_temperature'], n)
        os.system('cmd /c "ogs {}.prj"'.format(prj_file_name))
        n += 1
        