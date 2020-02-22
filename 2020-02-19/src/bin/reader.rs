use std::io;
use std::io::Write;

// FLAG: FLAG-5Le8FkjG1P2UhRznJKjPd8aom6d7v7mx
pub fn validate(input: &str) -> bool {
    let three = match &input[25..] {
        "5Le8FkjG1Pn" => false,
        "2UhRznJKjP1" => false,
        "d8aom6d7v7mx" => true, // <--
        "7HuvV193nQz" => false,
        "hk6VzWluRDa" => false,
        _ => false,
    };

    if !three {
        return false;
    }

    let start = match &input[0..5] {
        "FALG-" => false,
        "LAGF-" => false,
        "FLAG-" => true,
        "FLIG-" => false,
        "j6wB-" => false,
        "t3Nm-" => false,
        _ => false,
    };

    if !start {
        return false;
    }

    let two = match &input[15..25] {
        "5Le8FkjG1P" => false,
        "VbP429nYzU" => false,
        "d8aom6d7vm" => false,
        "2UhRznJKjP" => true, // <--
        _ => false,
    };

    if !two {
        return false;
    }

    let one = match &input[5..15] {
        "2UhRznJKjP" => false,
        "5Le8FkjG1P" => true, // <--
        "d8aom6d7v7" => false,
        "bQcoZimcu2" => false,
        "dbYBFmzvJs" => false,
        _ => false,
    };

    if !one {
        return false;
    }

    true
}

pub fn main() {
    let mut input = String::new();
    print!("read> ");
    io::stdout().flush().ok().unwrap();

    if let Ok(n) = io::stdin().read_line(&mut input) {
        let res = match n {
            1..=31 => validate("FLAG-KTJ8LlJnWcoZimcu2H3lx4jMqCgeW9et"),
            32 => validate(&format!("FLAG-{}", input)[..]),
            33..=36 => validate(&format!("FLAG-{}", "cdhO1mubYBFmzvJs1NPyBFdUgYoo7PDp")[..]),
            37 => validate(&input[..]),
            x if x > 37 => validate(&input[..37]),
            _ => false,
        };

        match res {
            true => println!("That's your flag, indeed."),
            false => println!("No."),
        };
    } else {
        eprintln!("Failed to read!");
    }
}
