use serde::{Deserialize, Serialize};
use std::convert::Infallible;
use warp::Filter;
use rand::prelude::*;
use rand::SeedableRng;
use base64::{encode};

const FLAG: &str  = "FLAG-XXXXXXXXXXXXXXXXXXXXXXXXX";
const BIND: ([u8; 4], u16) = ([0, 0, 0, 0], 3000);

#[derive(Serialize, Deserialize)]
pub struct License {
    pub user: String,
    pub key: String,
}

#[tokio::main]
async fn main() {
    let activation = warp::post()
        .and(warp::path("activate"))
        .and(warp::body::content_length_limit(1024))
        .and(warp::body::json())
        .and_then(validate);

    warp::serve(activation)
        .run(BIND)
        .await;
}


async fn validate(license: License) -> Result<impl warp::Reply, Infallible> {
    // Do all of the license validation stuff.
    let bytes: Vec<u64> = license.user.bytes().map(|b| b as u64).collect();
    let seed: u64 = bytes.iter().sum::<u64>() % 31;
    let mut rng: StdRng = SeedableRng::seed_from_u64(seed);
    let key: [u8; 32] = rng.gen();
    let key = encode(&key);

    match key == license.key {
        true => Ok(warp::reply::json(&FLAG)),
        false => Ok(warp::reply::json(&"Try again")),
    }
}
