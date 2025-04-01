within ;
package Mechanics

  model Vehicle
    parameter Real m = 1;
    parameter Real c = 1.9;
    parameter Real k = 0.05;
    parameter Real g = 9.81;
    parameter Real alpha = 20 * 3.14/180;
    parameter Real wagenheight = 2;
    parameter Real wagenwidth = 4;
    parameter Real hBall = sqrt(wagenheight^2+wagenwidth^2);
    
    Real x;
    Real y(start=20, fixed=true);
    Real R;
    Real vx;
    Real vy;
    Real s;
    Real ds;

  equation
    der(x) = vx;
    der(y) = vy;
    der(s) = ds;
    R = -k * sign(ds) * m * g * cos(alpha);
    der(ds) * m = R + m * g * sin(alpha);
    x = s * cos(alpha);
    y = -s * sin(alpha);

  end Vehicle;

  model ContactBall

    import Modelica.Units.SI.*;

    parameter Real m = 1;
    parameter Real r = 1;
    parameter Real c = 1e3; // Translational spring constant
    parameter Real d = 1e1; // Translational damping constant
    parameter Real g = 9.81;
      
    Real h; // Length
    Real v;
    Real x;
    Real vx;

    Modelica.Mechanics.Translational.Components.Fixed fixed
      annotation (Placement(transformation(extent={{-10,-86},{10,-66}})));
    Modelica.Mechanics.Translational.Components.Spring spring(s_rel0=r, c=c)
      annotation (Placement(transformation(extent={{-10,-10},{10,10}}, rotation=90,origin={-20,-50})));
    Modelica.Mechanics.Translational.Components.Mass mass(m=m)
      annotation (Placement(transformation(extent={{-10,-10},{10,10}}, rotation=90,origin={0,-10})));
    Modelica.Mechanics.Translational.Components.Damper damper(d=d)
      annotation (Placement(transformation(extent={{-10,-10},{10,10}}, rotation=90,origin={20,-50})));
    Modelica.Mechanics.Translational.Sources.Force force 
      annotation (Placement(transformation(extent={{-10,-10},{10,10}}, rotation=270,origin={0,28})));
    Modelica.Blocks.Sources.Constant const(k=-m*g)
      annotation (Placement(transformation(extent={{-60,60},{-40,80}})));

  equation
      der(x) = vx;
      der(vx) = 0;

      h = damper.s_rel * 1;
      v = damper.v_rel * 1;

    connect(const.y, force.f) annotation(
        Line(points = {{-38, 70}, {0, 70}, {0, 40}}, color = {0, 0, 127}));
    connect(force.flange, mass.flange_b) annotation(
        Line(points = {{0, 18}, {0, 0}}, color = {0, 127, 0}));
    connect(mass.flange_a, spring.flange_b) annotation(
        Line(points = {{0, -20}, {-20, -20}, {-20, -40}}, color = {0, 127, 0}));
    connect(mass.flange_a, damper.flange_b) annotation(
        Line(points = {{0, -20}, {20, -20}, {20, -40}}, color = {0, 127, 0}));
    connect(spring.flange_a, fixed.flange) annotation(
        Line(points = {{-20, -60}, {0, -60}, {0, -76}}, color = {0, 127, 0}));
    connect(damper.flange_a, fixed.flange) annotation(
        Line(points = {{20, -60}, {0, -60}, {0, -76}}, color = {0, 127, 0}));
  end ContactBall;

  model FlyingBall

    parameter Real r = 1;
    parameter Real g = 9.81;
    Real h(start=10);
    Real vx;
    Real x;
    Real vy;

  equation
      der(x) = vx;
      der(vx) = 0;  //acceleration of the ball in x direction
      der(h) = vy;
      der(vy) = -g;

  end FlyingBall;

  model Vehicle_struc
    extends Vehicle;
    Integer transitionId(start=0);

  equation
    when (y < 10) then
      transitionId = 1;
      terminate("soil contact");
    end when;
  end Vehicle_struc;

  model Ball_struc
    extends FlyingBall;
    Integer transitionId(start=0);

  equation
        when h < r then
          transitionId = 1;
          terminate("ball bounces on the ground");
        end when;

  end Ball_struc;

  model Contact_struc
    extends ContactBall;
    Integer transitionId(start=0);

  equation
        when (mass.s > r) then
          transitionId = 1;
          terminate("soil contact");
        end when;

  end Contact_struc;

  annotation (uses(Modelica(version="4.0.0")));

end Mechanics;
