function [Edges, I, B, A, b, r] = page_rank()
    Edges = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7;
             4, 6, 3, 4, 5, 5, 6, 7, 5, 6, 4, 6, 4, 7, 6];
    N = 7;
    d = 0.85;
    I = speye(N);
    B = sparse(Edges(2,:), Edges(1,:), 1, N, N);
    L = sum(B);
    A = spdiags(1 ./ L', 0, N, N);
    b = ones(N, 1) * (1-d)/N;

    M = I - d * B * A;

    r = M \ b;

    bar(r);
    title("Wartości PR wszystkich stron w sieci wyznaczonych przez page_rank.");
    xlabel("Numer strony");
    ylabel("PageRank");
end