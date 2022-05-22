// Gmsh project created on Thu Nov 04 10:01:46 2021
SetFactory("OpenCASCADE");

Point(1) = {20, 40, 0, 70};
Point(2) = {-20, 40, 0, 70};
Point(3) = {-20, 0, 0, 70};
Point(4) = {20, 0, 0, 70};

Point(6) = {0, 20, 0, 5};
Point(7) = {0, 20, -185, 5};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {6, 7};

Curve Loop(1) = {2, 3, 4, 1};
Plane Surface(1) = {1};




Transfinite Curve {3, 2, 1, 4} = 10 Using Progression 1;


//+
Extrude {0, 0, -185} {
  Surface{1}; Layers {100}; Recombine;
}

Point{6} In Surface{1};
Point{7} In Surface{6};

Transfinite Curve {5} = 100 Using Progression 1;
//Volume(1) = {1};
Line{5} In Volume{1};

Physical Curve("BHE_1", 8) = {5};
Physical Volume("BHE_soil", 9) = {1};