function frequency = wnTohz(wn)
    c = PhysicalConstant.LIGHT_SPEED;
    frequency = wn .* 100 .* c;
end

