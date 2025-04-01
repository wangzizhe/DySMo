within ;
package Domino
import Modelica.Units.SI.*;
constant Real pi = Modelica.Constants.pi;
  model DominoStone
    import Modelica.Units.SI.*;
    parameter Real X = 0.008;
    parameter Real Y = 0.024;
    parameter Real Z = 0.046;
    Real phi; // Angle
    Real phi_deg;
    parameter Real m = 0.01;
    parameter Real g = 9.81;
    parameter Real theta = m * (X^2 + Z^2)/3;
    parameter Real omega(start=0.0316, fixed=true); //Angular velocity
    parameter Real R = 0.5 * sqrt(X^2 + Z^2);
    Real T;
    Real x;
    Real z;
    //Real L;
    
  equation
    Modelica.Math.sin(phi) = x / Z;
    Modelica.Math.cos(phi) = z / Z;
    theta * der(omega) = T;
    der(phi) = omega;
    phi_deg = phi * 180 / pi;

    if phi < (90 / 180 * pi) then
      T = m * g * R * Modelica.Math.sin(phi);
    else
      T = 0;
    end if;

    when phi >= (90 / 180 * pi) then
      reinit(omega, 0);
    end when;

  end DominoStone;

  model Stones
    parameter Real D = 0.011; // Distance between domino stones
    parameter Integer active = 1;  // Count of active stones
    parameter Integer fallen = 0; // Count of fallen domino stones
    parameter Integer total = 5; // Total number of domino stones
    parameter Integer remaining = total - fallen - active;
    DominoStone Stones[active]; // Array of active domino stones
    Integer transitionId; // Transitions ID
    
  algorithm
    // When a domino stone is pushed over
    when Stones[active].x > D and remaining > 0 then
      transitionId := 1;
      terminate("Domino stone collision");
    // When the domino stone has fallen
    elsewhen Stones[1].phi_deg > 90 and active > 1 then
      transitionId := 2;
      terminate("Domino stone on the ground");
    // End of the simulation
    elsewhen Stones[1].phi_deg > 90 and active == 1 then
      transitionId := 3;
      terminate("End of simulation");
    end when;
  end Stones;

  annotation (uses(Modelica(version="4.0.0")));
end Domino;
