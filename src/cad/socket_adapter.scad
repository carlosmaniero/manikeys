$fn = $preview ? 15 : 200;

border=2;
offset_fix=0.1;

diode_r=1.4;
diode_wire_r=0.5;
diode_l=5;

diode_x=-2.54 - 2;
cube_size=13.6;

body_thickness=6;
cap_socket_height = 2;
cap_socket_width = cube_size + 4;

module diode(border) {
  translate([0, 0, (diode_l + border)/2]) {
    union() {
      cylinder(h = diode_l + border, r = diode_r, center=true);
      cylinder(h = diode_l * 100, r = diode_wire_r, center=true);
    }
  }
}

module cherryMxHole(){
  error=0.01; // 0.05 is the recommended tolerance
  hole_r=(1.5 + error) / 2;
  hole_l=500;
  distance=2;

  position = [
    [
      [3.81, 2.54],
      [3.81 + distance, -1.08]
    ],
    [
      [-2.54, 5.08],
      [-2.54 - distance, 1.08]
    ]
  ];

  union() {
    cylinder(h=hole_l, r=2, center=true);

    for (p = position) {
      hull() {
        for (point = p) {
          translate([point[0], point[1], 0.5 - 0.1]) {
            cylinder(r=hole_r, h=1.1, center=true);
          }
        }
      }
    }

    for (p = position) {
      for (point = p) {
        translate([point[0], point[1], 0]) {
          cylinder(h=hole_l, r=hole_r, center=true);
        }
      }
    }
  }
}

module diodeWirePath(){
  translate([diode_x, -cube_size/2, 0])
    cylinder(h=100, r=diode_wire_r * 2, center=true);
  translate([diode_x, cube_size/2, 0])
    cylinder(h=100, r=diode_wire_r * 2, center=true);
}

module cap_socket() {
  translate([0, 0, cap_socket_height/2 + 1]) {
    cube([cap_socket_width, cube_size, cap_socket_height], center=true);
  }
}

module led_placement() {
  pcb_radius = 5.05;
  pcb_thickness = 3;
  led_size = 5;
  led_height = 2;
  light_path = led_size - 2;
  
  translate([0, -pcb_radius, 4.5]) {
    cube([led_size, led_size, led_height], center=true);
    cube([light_path, light_path, 200], center=true);
    translate([0, 0, 0]) {
      cylinder(r=pcb_radius, h=pcb_thickness);
    }
  }
}

module body() {
  translate([0, 0, body_thickness/2])
    cube([cube_size, cube_size, body_thickness], center=true);
}

module full_body() {
  body();
  cap_socket();
}

color("#333333") {
  difference() {
    full_body();
    translate([diode_x, 0, 2.5])
      rotate([90, 0, 0])
        diode(border + offset_fix);
    cherryMxHole();
    diodeWirePath();
      
    led_placement();
  }
}

module socket() {
  size = cube_size + cap_socket_height * 2;

  translate([-size/2, -size/2, body_thickness - cap_socket_height/2]) {
    cube([size, size, cap_socket_height], center=true);
  }
}
