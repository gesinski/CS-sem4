function plot_residuum(A, b)
    [~, r_norm_Jacobi, iteration_count_Jacobi] = solve_Jacobi(A, b);
    [~, r_norm_Gauss_Seidel, iteration_count_GS] = solve_Gauss_Seidel(A, b);

    subplot(2, 1, 1);
    r_norm_Jacobi = r_norm_Jacobi(1:iteration_count_Jacobi + 1);
    semilogy(0:iteration_count_Jacobi, r_norm_Jacobi);
    xlabel('Liczba iteracji');
    ylabel('Norma residuum');
    title('Zmiana residuum - Metoda Jacobiego');
    grid on;

    subplot(2, 1, 2);
    r_norm_Gauss_Seidel = r_norm_Gauss_Seidel(1:iteration_count_GS + 1);
    semilogy(0:iteration_count_GS, r_norm_Gauss_Seidel);
    xlabel('Liczba iteracji');
    ylabel('Norma residuum');
    title('Zmiana residuum - Metoda Gaussa-Seidela');
    grid on;
    
end