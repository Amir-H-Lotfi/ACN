function frequency = wnTothz(wn)
    c = PhysicalConstant.LIGHT_SPEED;
    frequency = wn .* 100 .* c ./ PhysicalConstant.TERA;
end