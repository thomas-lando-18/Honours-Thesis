function C_k = C_k_Laplace(v,b,t)
% wagner function 
% Laplace Eqn
syms s 
t = t;
C_s = 1/2 + (0.0075*v/b)/(s + 0.0455*v/b)+(0.10055*v/b)/(s+0.3*v/b);
C_k = ilaplace(C_s);

C_k = double(subs(C_k));
end