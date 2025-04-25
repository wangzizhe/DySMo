within ;
package Pendulum
  model Pendulum_phi
    parameter Real m = 1;
    parameter Real g = 9.81;
    parameter Real L = 2;

    Real phi(start=0);
    Real dphi(start=2);
    Real x(start=-2, fixed=true);
    Real y;
    Real dx;
    Real dy;
    Real F;
  
  equation
    x = L * sin(phi);
    y = - L * cos(phi);
    dx = der(x);
    dy = der(y);
    dphi = der(phi);
    der(dphi) = -g/L * sin(phi);
    F = m * g * cos(phi) + m * L * dphi^2;

  end Pendulum_phi;

model Ball  
  parameter Real m = 1;
  parameter Real g = 9.81;
  parameter Real L = 2;

  Real x;
  Real y;
  Real vx;
  Real vy;
  Real r;

equation
  vx = der(x);
  vy = der(y);
  m * der(vx) = 0;
  m * der(vy) = -m * g;
  r = sqrt(x^2 + y^2);

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
  Real phi;
  Real dphi;
    
equation
  phi = asin(x/L);
  dphi = der(phi);

  when r > L then
    transitionId = 1;
    terminate("Ball to Pendulum");
  end when;
  
end Ball_struc;
  annotation(uses(Modelica(version="4.0.0")));
end Pendulum;
