function velocity_delta = velocity_difference(t)
% t - czas od startu rakiety
    if t <= 0
        error('Podany czas jest mniejszy lub równy zero.')
    end
    u = 2000;
    m0 = 150000;
    q = 2700;
    g = 1.622;
    M = 700;

    v = u * log(m0 / (m0 - q * t)) - g * t;

    velocity_delta = v - M;

end