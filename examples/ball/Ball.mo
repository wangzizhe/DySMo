within;

model Ball

model FlyingBall
  parameter Real r = 1;
   parameter Real g = 9.81;
   Real h(start=20);
   Real v;
   Integer transitionId(start=0);
equation
  der(h) = v;
  der(v) = -g;
  when h < 0 then
    transitionId = 1;
    terminate("Boden");
  end when;
end FlyingBall;

annotation (uses(Modelica(version="4.0.0")));

end Ball;
