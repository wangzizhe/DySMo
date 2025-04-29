within ;
package Clutch
  model ClutchBasic
    parameter Real j1=1;
    parameter Real j2=2;
    parameter Real k1=0.01;
    parameter Real k2=0.0125;
    Real w1(start = 1);
    Real w2(start = 1.5);
    Real f1; 
    Real f2;
  equation
    j1 * der(w1) = -k1 * w1 + f1;
    j2 * der(w2) = -k2 * w2 + f2;
    f1 + f2 = 0;
  end ClutchBasic;

  model ClutchUncoupled
    extends ClutchBasic;
    Integer transitionId(start=0);
  equation
    f1 = 0;
    when (time >= 5) then
      transitionId = 1;
      terminate("clutch coupled");
    end when;
  end ClutchUncoupled;

  model ClutchCoupled
    extends ClutchBasic;
    Integer transitionId(start=0);
  equation
    w1 - w2 = 0;
    when (time > 7) then
      transitionId = 1;
      terminate("clutch decoupled");
    end when;
  end ClutchCoupled;
end Clutch;
