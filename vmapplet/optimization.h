#include <math.h>
#include <array>
#include "plantgl/math/util_vector.h"

namespace optimization {

typedef std::array<float, 3> vec3;


vec3 rotate(float v3x, float v3y, float v3z, float angle, float vx, float vy, float vz)
{
    float c =  cosf(angle);
    float t2 =  1 - c;
    float t6 =  t2*v3x;
    float t7 =  t6*v3y;
    float s =  sinf(angle);
    float t9 =  s*v3z;
    float t11 = t6*v3z;
    float t12 = s*v3y;
    float t19 = t2*v3y*v3z;
    float t20 = s*v3x;
    float t24 = v3z*v3z;
    float R00 = c + t2*v3x*v3x;
    float R01 = t7 - t9;
    float R02 = t11 + t12;
    float R10 = t7 + t9;
    float R11 = c + t2*v3y*v3y;
    float R12 = t19 - t20;
    float R20 = t11 - t12;
    float R21 = t19 + t20;
    float R22 = c + t2*t24;
    return {R00*vx+R01*vy+R02*vz, R10*vx+R11*vy+R12*vz, R20*vx+R21*vy+R22*vz};
}

double second_moment_of_area_annular_section(double inner_radius, double thickness, double section)
{
    double rt = inner_radius + thickness;
    double rt2 = rt * rt;
    double rt4 = rt2 * rt2;
    double r = inner_radius;
    double r2 = r * r;
    double r4= r2 * r2;
    return  0.125 * (rt4 - r4) * (section + sinf(section));
}

double second_moment_of_area_circle(double radius)
{
    return 0.78539816339744828 * radius * radius * radius * radius;
}

double get_new_radius(double ra,double rb, double exponent = 2.49, double previous_rt = -1.)
{
    double rap = powf(ra, exponent);
    double rbp = powf(rb, exponent);
    double newrt =  powf(rap+rbp, 1./exponent);
    return newrt;
}

// cppyy runns but complains: IncrementalExecutor::executeFunction: symbol '_ZN3PGLmlERKNS_7Vector3ES2_' unresolved while linking symbol '__cf_11'!
// double reaction_wood_target(vec3 _up, vec3 _heading, vec3 _previous_heading)
// {
//     PGL::Vector3 up = PGL::Vector3(_up.at(0), _up.at(1), _up.at(2));
//     PGL::Vector3 heading = PGL::Vector3(_heading.at(0), _heading.at(1), _heading.at(2));
//     PGL::Vector3 previous_heading = PGL::Vector3(_previous_heading.at(0), _previous_heading.at(1), _previous_heading.at(2));
//     double cos_gh = PGL::Vector3(0.0, 0.0, 1.0) * heading;
//     double cos_pu = previous_heading * up;
//     double cos_ph = previous_heading * heading;
//     double inclination, percentage, r;

//     if (cos_pu*cos_ph >= 0.0)
//         inclination = acosf(cos_ph);
//     else
//         inclination = -acosf(cos_ph);

//     percentage  = 0.1635 * (1.0 - cos_gh) - 0.1778 * inclination;
//     r = 3.14159*2. * percentage;

//     if (r < 0.0)
//         r = 0.0;
//     else if (r > 3.14159)
//         r = 3.141459;

//     return r;
// }

}
