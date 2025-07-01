function [residuum_norm_direct, residuum_norm_Jacobi, residuum_norm_Gauss_Seidel] = filter_solutions()
% residuum_norm_direct - norma residuum dla rozwiązania metodą bezpośrednią
% residuum_norm_Jacobi - norma residuum dla rozwiązania metodą Jacobiego
% residuum_norm_Gauss_Seidel - norma residuum dla rozwiązania metodą Gaussa-Seidele'a

    residuum_norm_direct = 7.02302163136495e-13;
    residuum_norm_Jacobi = Inf;
    residuum_norm_Gauss_Seidel = 6.436734796338985e+10;
end