// Gmsh project created on Thu Nov 04 10:01:46 2021
SetFactory("OpenCASCADE");

Point(1) = {20, 40, 0, 40};
Point(2) = {-20, 40, 0, 40};
Point(3) = {-20, 0, 0, 40};
Point(4) = {20, 0, 0, 40};
Point(5) = {0, 20, 0, 0.2};

Point(6) = {0, 20, -17, 1};
Point(7) = {0, 20, -185, 1};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {6, 7};

Curve Loop(1) = {2, 3, 4, 1};
Plane Surface(1) = {1};
Point{5} In Surface{1};

Extrude {0, 0, -185} {
  Surface{1}; Layers {185}; Recombine;
}
Transfinite Curve {3, 2, 1, 4} = 6 Using Progression 1;



Line{5} In Volume{1};

Physical Curve("BHE_1", 1) = {5};
Physical Volume("BHE_soil", 2) = {1};