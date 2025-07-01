load filtr_dielektryczny.mat;
[x_direct,r_norm_direct] = solve_direct(A, b);
[x_Jacobi,r_norm_Jacobi] = solve_Jacobi(A, b);
[x_Gauss_Seidel,r_norm_Gauss_Seidel] = solve_Gauss_Seidel(A, b);

plot_residuum(A, b);

print -dpng residuum.png