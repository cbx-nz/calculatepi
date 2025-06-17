use rug::{Assign, Float};
use std::fs::File;
use std::io::Write;

const PRECISION: u32 = 10000; // in bits (~3.3 bits per digit, this gives ~3000 digits)
const LINE_LENGTH: usize = 1000;

fn calculate_pi(digits: usize) -> String {
    let mut pi = Float::with_val(PRECISION, 0);
    let mut k = 0;
    let mut factor = Float::with_val(PRECISION, 1);

    while k < digits / 14 + 1 {
        let kf = Float::with_val(PRECISION, k as f64);
        let top = Float::with_val(PRECISION, 120 * factor.clone());
        let bottom = Float::with_val(PRECISION, (2 * k + 1) * 16f64.powi(k as i32));
        pi += &top / &bottom;
        factor *= (2 * k + 1) as u32;
        k += 1;
    }

    format!("{:.digits$}", pi, digits = digits)
}

fn generate_html(pi_digits: &str, output_file: &str) {
    let mut html = String::from(r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Digits of Pi</title>
<style>
    body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
    #viewer { max-height: 600px; overflow-y: auto; border: 1px solid #0f0; padding: 10px; background: #111; }
    .line { display: flex; }
    .linenum { width: 80px; color: #999; }
    .digits { white-space: pre-wrap; word-break: break-word; flex: 1; }
</style>
</head>
<body>
<h1>Digits of Pi</h1>
<div id="viewer">
"#);

    for (i, chunk) in pi_digits.chars().collect::<Vec<_>>().chunks(LINE_LENGTH).enumerate() {
        let line_num = i * LINE_LENGTH + 1;
        let line_str: String = chunk.iter().collect();
        html.push_str(&format!(
            r#"<div class="line"><div class="linenum">{}</div><div class="digits">{}</div></div>"#,
            line_num, line_str
        ));
    }

    html.push_str("</div></body></html>");

    let mut file = File::create(output_file).expect("Cannot write file");
    file.write_all(html.as_bytes()).expect("Failed to write HTML");
}

fn main() {
    let digits_to_calc = 3000; // You can increase this with higher PRECISION
    println!("Calculating {} digits of Pi...", digits_to_calc);
    let pi = calculate_pi(digits_to_calc);
    println!("Writing to HTML...");
    generate_html(&pi, "pi.html");
    println!("✅ Done. Open pi.html to view.");
}