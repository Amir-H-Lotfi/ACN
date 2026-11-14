function loss = spreading_loss(frequency, distance)

c = PhysicalConstant.LIGHT_SPEED;

loss = 20 .* log10( ...
    (4 .* pi .* frequency .* distance) ./ c ...
    );

end