function [x,r_norm,iteration_count] = solve_Jacobi(A, b)

N = size(A, 1);

iteration_count = 0;

L = tril(A, -1);
U = triu(A, 1);
D = diag(diag(A));

M = -(D \ (L + U));
w = D \ b;
x = ones(N,1);
r_norm = [];


inorm = norm(A * x-b);
r_norm = inorm;
while(inorm>1e-12 && iteration_count<1000)
    x = M * x + w;
    inorm = norm(A * x-b);
    iteration_count = iteration_count+1;
    r_norm = [ r_norm, inorm ];
    
end
end