function Forces = Aerodynamic_Forces_Calculation()
    
    C = CkCalculation(k);
    Forces.Coefficients.L_h = 1 - complex(0,2)*v/(b*omega)*C;

end