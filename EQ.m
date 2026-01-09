function EQ(audioFile, gainArray, savedName)
clc;
clf;

[x, fs] = audioread(audioFile);
t = (0:length(x)-1) / fs;
nyq = fs/2;

G = 10^(gainArray(8)/20);
x_down = x*G;

G_sub = 10^(gainArray(1)/20);
[n, Wn] = buttord(60 / nyq, 80 / nyq, 0.5, 60);
[z, p, k] = butter(n, Wn, 'low');
[sos, g] = zp2sos(z, p, k);
y_sub = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

G_bass = 10^(gainArray(2)/20);
Wp_bass = [60 275] ./ nyq;
[z, p, k] = butter(6, Wp_bass, 'bandpass');
[sos, g] = zp2sos(z, p, k);
y_bass = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

G_lowMids = 10^(gainArray(3)/20);
Wp_low = [250 500] ./ nyq;
[z, p, k] = butter(6, Wp_low, 'bandpass');
[sos, g] = zp2sos(z, p, k);
y_lowMids = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

G_mids = 10^(gainArray(4)/20);
Wp_mids = [500 2000] ./ nyq;
[z, p, k] = butter(6, Wp_mids, 'bandpass');
[sos, g] = zp2sos(z, p, k);
y_mids = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

G_high = 10^(gainArray(5)/20);
Wp_high = [2000 4000] ./ nyq;
[z, p, k] = butter(6, Wp_high, 'bandpass');
[sos, g] = zp2sos(z, p, k);
y_high = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

G_pres = 10^(gainArray(6)/20);
Wp_pres = [4000 6000] ./ nyq;
[z, p, k] = butter(6, Wp_pres, 'bandpass');
[sos, g] = zp2sos(z, p, k);
y_pres = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

G_air = 10^(gainArray(7)/20);
Wp_air = [6000 20000] ./ nyq;
[z, p, k] = butter(n, Wp_air, 'bandpass'); 
[sos, g] = zp2sos(z, p, k);
y_air = filtfilt(sos, g, x_down);
Hd = dfilt.df2tsos(sos, g);
% fvtool(Hd, 'Fs', fs);

y = x_down + (G_sub - 1).*y_sub + (G_bass - 1).*y_bass...
    + (G_lowMids - 1)*y_lowMids + (G_mids - 1)*y_mids...
    + (G_high - 1)*y_high + (G_pres - 1)*y_pres + (G_air - 1)*y_air;

audiowrite(savedName, y, fs);% Save

figure(1);
subplot(2,1,1);
plot(t, x);
xlabel('Time (seconds)');
ylabel('Amplitude');
title('Original Audio Signal');
legend('Left Channel', 'Right Channel');
ylim([-1 1]);

subplot(2,1,2);
plot(t, y);
xlabel('Time (seconds)');
ylabel('Amplitude');
title('Filtered Audio Signal');
legend('Left Channel', 'Right Channel');
ylim([-1 1]);

end