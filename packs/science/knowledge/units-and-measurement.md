# Units and Measurement

## SI base units

Seven base units define all others: metre (length), kilogram (mass), second
(time), ampere (electric current), kelvin (temperature), mole (amount of
substance), candela (luminous intensity). Every other SI unit is a combination
of these. A newton is kg·m/s². A joule is a newton-metre, so kg·m²/s². A watt is
a joule per second.

Knowing the composition of a derived unit is often enough to reconstruct a
forgotten formula. Since a joule is kg·m²/s², any expression for energy must
reduce to mass times velocity squared in its dimensions — which is why both
½mv² and mgh work, and why mv would not.

## Dimensional analysis

Every term in a valid equation must carry the same dimensions. This is the
cheapest error check in physics: if one side reduces to metres per second and
the other to metres, the equation is wrong regardless of how the algebra looked.

Dimensional analysis also constrains unknown relationships. If a pendulum's
period can depend only on length L, mass m, and gravity g, then the only
combination yielding units of time is √(L/g) — which correctly predicts that
period does not depend on mass.

Arguments of transcendental functions must be dimensionless. You can take the
sine of an angle or the logarithm of a ratio, never of three metres.

## Significant figures

The precision of a result is limited by the least precise input. For
multiplication and division, the result carries as many significant figures as
the input with the fewest. For addition and subtraction, match the fewest
decimal places instead.

Leading zeros are never significant; 0.0042 has two. Trailing zeros after a
decimal point are significant; 4.200 has four. Trailing zeros in a whole number
are ambiguous, which is one reason scientific notation exists: 4.2 × 10³ says
two figures, 4.200 × 10³ says four.

Carry extra digits through intermediate steps and round only at the end.
Rounding early compounds error.

## Scientific notation and prefixes

A number in scientific notation is written as a coefficient between 1 and 10
times a power of ten. Multiplying adds exponents, dividing subtracts them.

Common prefixes step by factors of a thousand: kilo (10³), mega (10⁶), giga
(10⁹), tera (10¹²) going up; milli (10⁻³), micro (10⁻⁶), nano (10⁻⁹), pico
(10⁻¹²) going down. Centi (10⁻²) is the notable exception to the thousand-step
pattern and survives mainly in the centimetre.
