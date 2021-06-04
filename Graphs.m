clear;
clc;
clf;
%%
% Resources
% CANDLES: https://au.mathworks.com/help/finance/candle.html
% TIMETABLES: https://au.mathworks.com/help/finance/using-timetables-in-finance.html
% COLORS: http://math.loyola.edu/~loberbro/matlab/html/colorsInMatlab.html

load('data.mat')
dateTime = datetime(Time, 'convertfrom','posixtime');
TMW_HA = timetable(O_ha',H_ha',L_ha',C_ha', 'VariableNames',{'Open','High','Low','Close'},'RowTimes',dateTime');

figure(1);
    h_HA = candle(TMW_HA);
    hold on
    
    plot(dateTime, BOLL, 'm', dateTime, BOLU, 'm');
    
    plot(dateTime, MA_5, 'Color', [0.9290, 0.6940, 0.1250]);
    plot(dateTime, MA_9, 'Color', [0.4660, 0.6740, 0.1880]);
    plot(dateTime, MA_20, 'Color', [0.6350, 0.0780, 0.1840]);
    plot(dateTime, MA_50, 'Color', [0.8500, 0.3250, 0.0980]);
    plot(dateTime, MA_200, 'Color', [0.4940, 0.1840, 0.5560]) ;
    plot(dateTime, TEMA_8, 'b');
    hold off;
    title('Candlestick Chart');
    xlabel('Date');
    ylabel('Price (USD)');
    ylim ([0, inf]);
    grid on;
    %legend({'Heiken Ashi', 'BOLL', 'BOLU', 'MA5', 'MA9', 'MA20', 'MA50', 'MA200'}, 'Location', 'southeast')
    
figure(2);
    plot(dateTime, RSI, 'Color', [0.4940, 0.1840, 0.5560]);
    hold on;
    yline(30,'g','--');
    yline(70,'g','--');
    hold off;
    title('Relative Strength Index (RSI)');
    xlabel('Date');
    ylabel('RSI');
    grid on;
    ylim ([0, 100]);

figure(3);
    plot(dateTime, MACD)
    hold on
    plot(dateTime, MACD_EMA_9)
    %bar(datetime, MACD_histogram)
    yline(0,'r');
    hold off
    grid on;
    
% Trade Signals
figure(1);
    buyID = find(S1_Trade == true);
    sellID = find(S1_Trade == false);
    
    S1_ID = S1_ID + 1; % MATLAB array index starts from 1
    S1_Time = datetime(S1_Time, 'convertfrom','posixtime');
    hold on
    plot(S1_Time(buyID), S1_TradePrice(buyID),'s','MarkerSize',10, 'MarkerEdgeColor','green','MarkerFaceColor', [0, 0.75, 0],'LineStyle', 'none' );
    plot(S1_Time(sellID), S1_TradePrice(sellID),'s','MarkerSize',10, 'MarkerEdgeColor','red','MarkerFaceColor', 'red','LineStyle', 'none' );
    hold off
    
    
   
    