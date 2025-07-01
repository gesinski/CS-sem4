function [matrix_sizes, condition_numbers, interpolation_error_exact, interpolation_error_perturbed] = ...
        ill_conditioning_effects()
% Określa wpływ współczynnika uwarunkowania macierzy Vandermonde'a na dokładność interpolacji.
% Generuje trzy wykresy ilustrujące uwarunkowanie macierzy i błędy interpolacji.
%
% matrix_sizes - rozmiar testowych macierzy Vandermonde'a
% condition_numbers - współczynniki uwarunkowania testowych macierzy Vandermonde'a
% interpolation_error_exact - maksymalna różnica między referencyjnymi
%       a obliczonymi współczynnikami wielomianu, gdy b zawiera
%       wartości funkcji kwadratowej 
% interpolation_error_perturbed - maksymalna różnica między referencyjnymi
%       a obliczonymi współczynnikami wielomianu, gdy b zawiera
%       zaburzone wartości funkcji kwadratowej 


    % Inicjalizacja danych
    matrix_sizes = 5:100;
    num_points = length(matrix_sizes);

    % Prealokacja danych
    condition_numbers = zeros(1, num_points);
    interpolation_error_exact = zeros(1, num_points);
    interpolation_error_perturbed = zeros(1, num_points);

    %===========================================================================
    % Część 1: Obliczanie współczynnika uwarunkowania macierzy Vandermonde'a
    %===========================================================================
    for index = 1:num_points
        size_n = matrix_sizes(index);
        interpolation_nodes = linspace(-1, 1, size_n)';
        V = get_vandermonde_matrix(interpolation_nodes);

        condition_numbers(index) = cond(V);
    end

    % Szukam progu złego uwarunkowania
    threshold_index = find(condition_numbers >= 1e8, 1);

    % Wykres 1
    tiledlayout(3, 1, 'Padding', 'compact', 'TileSpacing', 'compact');
    nexttile;
    semilogy(matrix_sizes, condition_numbers);
    title('Zależność współczynnika uwarunkowania macierzy Vandermondea od rozmiaru macierzy');
    xlabel('Rozmiar macierzy');
    ylabel('Współ. uwarunkowania');
    hold on;

    if ~isempty(threshold_index)
        size_threshold = matrix_sizes(threshold_index);
        xline(size_threshold, '--', 'cond(V) > 10^8', 'LabelOrientation',...
            'horizontal', 'LabelVerticalAlignment', 'top',...
            'LabelHorizontalAlignment', 'left', 'Color', [0.494 0.184 0.556]);
    end

    %===========================================================================
    % Część 2: Obliczenie błędu interpolacji dla dokładnych danych (f(x)=x^2)
    %===========================================================================
    for index = 1:num_points
        size_n = matrix_sizes(index);
        interpolation_nodes = linspace(-1, 1, size_n)';
        V = get_vandermonde_matrix(interpolation_nodes);

        a2 = 1;
        b_exact = a2*interpolation_nodes.^2; % f(x) = a2*x^2

        reference_coefficients = [0; 0; a2; zeros(size_n - 3, 1)];
        computed_coefficients = V \ b_exact

        interpolation_error_exact(index) = max(abs(computed_coefficients - reference_coefficients));
    end

    % Wykres 2
    nexttile;
    plot(matrix_sizes, interpolation_error_exact);
    title('Maksymalny błąd współczynnika wielomianu funkcji kwadratowej od rozmiaru macierzy');
    xlabel('Rozmiar macierzy');
    ylabel('Max błąd wsp. wielomianu');
    hold on;

    %===========================================================================
    % Część 3: Obliczenie błędu interpolacji dla danych zaburzonych
    %===========================================================================
    for index = 1:num_points
        size_n = matrix_sizes(index);
        interpolation_nodes = linspace(-1, 1, size_n)';
        V = get_vandermonde_matrix(interpolation_nodes);

        a2 = 1;
        b_perturbed = a2*interpolation_nodes.^2 + rand(size_n, 1) * 1e-9;
        reference_coefficients = [0; 0; a2; zeros(size_n - 3, 1)];
        computed_coefficients = V \ b_perturbed

        interpolation_error_perturbed(index) = max(abs(computed_coefficients - reference_coefficients));
    end

    % Wykres 3
    nexttile;
    semilogy(matrix_sizes, interpolation_error_perturbed);
    title('Maksymalny błąd współ. wielomianu w zleżności od rozmiaru macierzy (dane z szumem)');
    xlabel('Rozmiar macierzy');
    ylabel('Max błąd wsp. wielomianu');
    hold on;
end

function V = get_vandermonde_matrix(x)
    % Buduje macierz Vandermonde’a na podstawie wektora węzłów interpolacji x.
    N = length(x);
    V = ones(N, N);
    for i = 2:N
        V(:, i) = x.^(i-1);
    end
end