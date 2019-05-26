#!/bin/bash

~/.cargo/bin/wasm-pack build --no-typescript --release --out-dir ../website/wasm/ --target no-modules
