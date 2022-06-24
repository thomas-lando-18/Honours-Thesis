% Test for Theodorsen
sys.constants = system_constants();
state.matrices = StateSpaceBuild(sys.constants);

% Build Main Matrices
A_p = (state.matrices.A-state.matrices.D)\state.matrices.E;
B_p = (state.matrices.A-state.matrices.D)\(state.matrices.F-state.matrices.C);

% Build A matrix (System) and B matrix (Control)
A = [A_p(1,1) A_p(1,3)  B_p(1,1) B_p(1,3);
     A_p(3,1) A_p(3,3)  B_p(3,1) B_p(3,3);
     1 0 0 0;
     0 1 0 0];
    