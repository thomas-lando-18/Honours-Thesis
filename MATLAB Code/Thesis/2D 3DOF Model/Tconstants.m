function T = Tconstants(a, c)
% This funtion outputs a structure of size 14 containing values of T1 to
% T14

    T{1} = -1/3*sqrt(1-c^2)*(2+c^2)+c*acos(c);
    T{2} = c*(1-c^2)-sqrt(1-c^2)*(1+c^2)*acos(c)+c*(acos(c))^2;
    T{3} = -(1/8 + c^2)*(acos(c))^2 + 1/4*c*sqrt(1-c^2)*acos(c)*(7+2*c^2)...
        -1/8*(1-c^2)*(5*c^2+4);
    T{4} = -acos(c)+c*sqrt(1-c^2);
    T{5} = -(1-c^2)-(acos(c))^2 + 2*c*sqrt(1-c^2)*acos(c);
    T{6} = T{2};
    T{7} = -(1/8+c^2)*acos(c)+1/8*c*sqrt(1-c^2)*(7+2*c^2);
    T{8} = -1/3*sqrt(1-c^2)*(2*c^2+1)+c*acos(c);
    T{9} = 1/2*(1/3*(sqrt(1-c^2))^3+ a*T{4});
    T{10} = sqrt(1-c^2) + acos(c);
    T{11} = acos(c)*(1-2*c)+sqrt(1-c^2)*(2-c);
    T{12} = sqrt(1-c^2)*(2+c)- acos(c)*(2*c+1);
    T{13} = 1/3*(-T{7}-(c-a)*T{1});
    T{14} = 1/16-1/2*a*c;

end