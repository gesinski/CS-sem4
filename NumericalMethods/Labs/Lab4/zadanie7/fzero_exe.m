options = optimset('Display','iter');
fzero(@tan,4.5, options);
fzero(@tan,6.0, options);