function impedance_delta = impedance_difference(f)
% Wyznacza moduł impedancji równoległego obwodu rezonansowego RLC pomniejszoną o wartość M.
% f - częstotliwość
    if f <= 0
        error('Podana częstotliwość jest mniejsza lub równa zero.')
    end
    R = 525;
    C = 7e-5;
    L = 3;
    M = 75;

    Z = 1 / (sqrt(1/(R^2) + (2*pi*f*C - 1 / (2*pi*f*L))^2));

    impedance_delta = Z - M;

end