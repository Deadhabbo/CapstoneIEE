data1 = readtable('coordenadas3.csv');

x1 = flip(data1.Var1);
x2 = flip(data1.Var3);
y1 = flip(data1.Var2);
y2 = flip(data1.Var4);

u = [x1(1:end-1) - x2(1:end-1), y1(1:end-1) - y2(1:end-1)];  % Entradas
y = [x1(2:end), y1(2:end)];   % Salidas
Ts = 0.01;  % Intervalo de muestreo en segundos.

data2 = iddata(y, u, Ts);

% órdenes del modelo
na = [1 1; 1 1];
nb = [1 154; 4 133];
nk = [0 0;0 0];


net = idWaveletNetwork('NumberOfUnits', 'auto');


orders = [na nb nk];
nl = net;
model7 = nlarx(data2, orders, 'OutputFcn', nl);




compare(data2, model7);



