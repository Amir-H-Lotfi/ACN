function loss = absorption_loss(absorption_coefficient,distance)
    loss = exp(absorption_coefficient .* distance)
end