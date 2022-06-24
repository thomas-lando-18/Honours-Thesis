% Theodorseon Model for flutter

% P.Yang Parameters
m = 5.12;
c = 0.5;
a = -0.5;
b = 0.799;

S_beta = 0.00086;
S_alpha = 0.0309;

C_alpha = 3.12;
C_beta = 357.1^2;
C_h = 2542;

I_alpha = 0.0031;
I_beta = 0.000021;

% Force inputs
M_alpha = 0;
M_beta = 0;
P = 0;

% EOM

F = [M_alpha; M_beta; P];

A = [I_alpha, (I_beta + b(c-a)*S_beta), S_alpha;
     (I_beta + b(c-a)*S_beta), I_beta, S_beta;
     S_alpha, S_beta, m];

B = zeros(3,3);

C = [C_alpha, 0, 0;
     0, C_beta, 0;
     0, 0, C_h];

% Theodoreson Constants
T = Tconstants(a,c);

% C(k) function
 k = 0;
 C = CkCalculation(k);

% Atmospheric Conditions
Alt = 0;
Mach = 0.5;
[rho, v] = GetAtmosVal(Alt, Mach);

% C Calculation
C = C_k_Laplace(v, b, 0.01);

% Aerodynamic Forces and Moments 

D = [-rho*b^4*pi*(1/8+a^2), rho*b^4*(T{7}+(c-a)*T{1}), rho*b^3*a*pi;
    -rho*b^4*2*T{13}, rho*b^4*1/pi*T{3}, rho*b^3*T{1};
    rho*b^4*pi*a, -rho*b^3*T{1}, -rho*b^2*pi];

E = [-rho*b^3*pi*(1/2-a)*v+2*rho*v*b^3*pi*(1/4-a^2)*C, ...
    -rho*b^3*(T{1}-T{8}-(c-a)*T{4}+1/2*T{11})*v+rho*v*b^3*(a+1/2)*C*T{11}, ...
    2*rho*v*b^2*pi*(a+1/2)*C;
    -rho*b^3*(-2*T{9}-T{1}+T{4}*(a-1/2))*v-rho*v*b^3*T{12}*C*(1/2-a), ...
    rho*b^3*1/(2*pi)*v*T{4}*T{11}-rho*v*b^3*T{12}*C*1/(2*pi)*T{11}, ...
    -rho*v*b^2*T{12}*C;
    -rho*b^2*v*pi-2*pi*rho*v*b^2*C*(1/2-a),...
    rho*b^2*v*T{4}-rho*v*b^2*C*T{11}, ...
    -2*pi*rho*v*b*C];

G = [2*rho*v^2*b^2*pi*(a+1/2)*C, ...
    -rho*b^2*(T{4}+T{10})*v^2+2*rho*v^2*b^2*(a+1/2)*C*T{10}, 0;
    -rho*v^2*b^2*T{12}*C, ...
    -rho*b^2*1/pi*v^2*(T{5}-T{4}*T{10})-rho*v^2*b^2*T{12}*C*1/pi*T{10}, 0;
    -2*pi*rho*v^2*b*C, -2*rho*v^2*b*C*T{10}, 0];

A_state = [(A-D)\(E-B), (A-D)\(G-C);
            eye(3), zeros(3,3)];
% Equilibrium Point
h = 0.01;

syms alpha beta ad bd hd
qd = [ad; bd; hd];
q = [alpha; beta; h];

Eqn1 = 0 == (A-D)\(E-B)*qd + (A-D)\(G-C)*q;
sol = solve([Eqn1], [alpha, beta, ad, bd, hd]);


alpha = double(sol.alpha);
beta = double(sol.beta);
ad = double(sol.ad);
bd = double(sol.bd);
hd = double(sol.hd);

qd = [ad; bd; hd];
q = [alpha; beta; h];

X = [qd; q];
Xd = A_state*X;

