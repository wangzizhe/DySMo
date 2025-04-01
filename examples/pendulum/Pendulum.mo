within ;
package Pendulum
  import Modelica.Math.sin;
  import Modelica.Math.asin;
  import Modelica.Math.cos;
  import Modelica.Units.SI.*;
  import Modelica.Utilities.Streams.print;
  model Pendulum_phi
    // Pendulum with equations related to the angle phi
    Angle phi(start=0);
    AngularVelocity dphi(start=-2);
    parameter Real g = 9.81;
    parameter Mass m = 1;
    Length x(start=2, fixed=true);
    Length y;
    Velocity dx;
    Velocity dy;
    Real D = 0.0;
    Length L = 2;
    Force F;
  
  equation
    x = sin(phi) * L;
    y = -cos(phi) * L;
    dy = der(y);
    dx = der(x);
    dphi = der(phi);
    der(dphi) = -g/L * sin(phi) - D * g/L * der(phi);
    F = m * g * cos(phi) + m * L * dphi^2;

  end Pendulum_phi;

model Ball  
  // Throwing the ball
  Real x;
  Real y;
  Real vx;
  Real vy;
  parameter Real m = 1;
  constant Real g = 9.81;
  parameter Real c0 = 0;
  parameter Real L = 2;

equation
  vx = der(x);
  vy = der(y);
  m * der(vx) = 0;
  m * der(vy) = -g * m;

end Ball;

model Pendulum_struc
  extends Pendulum_phi;
  Integer transitionId(start=1);

equation
    when F <= 0 or terminal() then
    transitionId = 1;
    terminate("Pendulum to ball");
    end when;

end Pendulum_struc;

model Ball_struc
  extends Ball;
  Integer transitionId(start=0);
  Angle phi;
  AngularVelocity dphi;
    Real r;
    
equation
  phi = asin(x/L);
  dphi = der(phi);
  r = sqrt(x^2 + y^2);

  when r > L then
    transitionId = 1;
    terminate("Ball to Pendulum");
  end when;
  
end Ball_struc;
  annotation(uses(Modelica(version="4.0.0")));
end Pendulum;
