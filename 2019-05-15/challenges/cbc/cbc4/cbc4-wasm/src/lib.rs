use rand::RngCore;
use rand::rngs::OsRng;

use x25519_dalek::{ x25519, X25519_BASEPOINT_BYTES };
use aes::Aes256;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;

use wasm_bindgen::prelude::*;
use wasm_bindgen::JsCast;
use wasm_bindgen::JsValue;
use wasm_bindgen_futures::future_to_promise;
use wasm_bindgen_futures::JsFuture;
use futures::{future, Future};
use js_sys::Promise;
use web_sys::{Request, RequestInit, Response};
use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Serialize, Deserialize)]
pub struct KeyExchangeRes {
    pub id: String,
    pub public_key: String,
}

#[derive(Serialize, Deserialize)]
pub struct Data {
    pub data: String,
}

#[derive(Clone)]
struct KeyData {
    pub id: String,
    pub key: Vec<u8>,
}

#[derive(Serialize, Deserialize)]
pub struct PasswordRequest {
    pub id: String,
    pub encrypted_password: String,
}

#[wasm_bindgen(start)]
pub fn start() -> Result<(), JsValue> {
    create_dom()?;

    let key = key_exchange();
    future_to_promise( key.and_then(|key| {
        set_button_handlers(key).unwrap();
        future::ok(JsValue::null())
    }));
    future_to_promise(get_leak());
    Ok(())
}

fn create_dom() -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    let body = document.body().expect("document should have a body");

    // Generate HTML
    let title = document.create_element("h1")?;
    title.set_inner_html("AES-CBC 4!");

    body.append_child(&title)?;

    let p = document.create_element("p")?;
    p.set_inner_html("This challenge is a bit different from the last one. Don't forget to check the server code!");
    body.append_child(&p)?;

    let p = document.create_element("p")?;
    p.set_inner_html("You are able to verify your password with the server. However, you've been able to intercept the following request:");
    body.append_child(&p)?;

    let leak_box = document.create_element("h2")?;
    leak_box.set_id("leak-box");
    body.append_child(&leak_box)?;

    let p = document.create_element("p")?;
    p.set_inner_html("Break it. You can use this to send your password:");
    body.append_child(&p)?;

    let password_input = document.create_element("input")?;
    password_input.set_id("password-input");
    body.append_child(&password_input)?;

    let password_btn = document.create_element("button")?;
    password_btn.set_inner_html("Send");
    password_btn.set_id("password-btn");
    password_btn.set_attribute("disabled", "true")?;
    body.append_child(&password_btn)?;

    let password_box = document.create_element("div")?;
    password_box.set_id("password-box");
    body.append_child(&password_box)?;

    let p = document.create_element("p")?;
    p.set_inner_html("You can verify your flag here:");
    body.append_child(&p)?;

    let flag_input = document.create_element("input")?;
    flag_input.set_id("flag-input");
    body.append_child(&flag_input)?;

    let flag_btn = document.create_element("button")?;
    flag_btn.set_inner_html("Verify");
    flag_btn.set_id("flag-btn");
    flag_btn.set_attribute("disabled", "true")?;
    body.append_child(&flag_btn)?;

    let flag_box = document.create_element("div")?;
    flag_box.set_id("flag-box");
    body.append_child(&flag_box)?;

    Ok(())
}

fn get_leak() -> Box<Future<Item=JsValue, Error=JsValue>> {
    let window = web_sys::window().unwrap();
    let mut opts = RequestInit::new();
    opts.method("GET");

    let request = Request::new_with_str_and_init(
        "./api/leak",
        &opts,
    ).unwrap();

    let request_promise = window.fetch_with_request(&request);

    let future = JsFuture::from(request_promise)
        .and_then(|resp_value| {
            let resp: Response = resp_value.dyn_into().unwrap();
            resp.json()
        })
        .and_then(|json_value: Promise| {
            // Convert this other `Promise` into a rust `Future`.
            JsFuture::from(json_value)
        })
        .and_then(move |json| {
            let leak: Data = json.into_serde().unwrap();
            let leak_box = window.document().unwrap().get_element_by_id("leak-box").unwrap();
            leak_box.set_inner_html(&leak.data);
            future::ok(JsValue::null())
        });
    Box::new(future)
}

fn key_exchange() -> Box<Future<Item=KeyData, Error=JsValue>>{
    let mut rng = OsRng::new().unwrap();
    let mut private_key = [0u8; 32];
    rng.fill_bytes(&mut private_key);

    let public_key = x25519(private_key.clone(), X25519_BASEPOINT_BYTES);

    let window = web_sys::window().expect("no global `window` exists");

    let exchange_data = json!(Data { data: base64::encode(&public_key) }).to_string();
    let mut opts = RequestInit::new();
    opts.method("POST");
    opts.body(Some(&JsValue::from_str(&exchange_data)));

    let request = Request::new_with_str_and_init(
        "./api/key-exchange",
        &opts,
    ).unwrap();

    request.headers().set("Content-Type", "application/json").unwrap();

    let request_promise = window.fetch_with_request(&request);

    let future = JsFuture::from(request_promise)
        .and_then(|resp_value| {
            let resp: Response = resp_value.dyn_into().unwrap();
            resp.json()
        })
        .and_then(|json_value: Promise| {
            // Convert this other `Promise` into a rust `Future`.
            JsFuture::from(json_value)
        })
        .and_then(move |json| {
            // Use serde to parse the JSON into a struct.
            let key_ex_res: KeyExchangeRes = json.into_serde().unwrap();

            let mut public_key = [0u8;32];
            public_key.copy_from_slice(&base64::decode(&key_ex_res.public_key).unwrap()[0..32]);

            let key = KeyData{
                id: key_ex_res.id,
                key: Vec::from(&x25519(private_key, public_key)[0..32])
            };

            future::ok(key)
        });
    Box::new(future)
}

fn set_button_handlers(key: KeyData) -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    {
        let password_btn_handler = Closure::wrap(Box::new(move |_: web_sys::MouseEvent| {
            future_to_promise(send_password(key.clone()));
            ()
        }) as Box<dyn FnMut(_)>);

        let password_btn = document.get_element_by_id("password-btn").unwrap();
        password_btn.add_event_listener_with_callback("click", password_btn_handler.as_ref().unchecked_ref())?;

        password_btn.remove_attribute("disabled")?;

        password_btn_handler.forget();
    }
    {
        let flag_btn_handler = Closure::wrap(Box::new(move |_: web_sys::MouseEvent| {
            future_to_promise(check_flag());
            ()
        }) as Box<dyn FnMut(_)>);

        let flag_btn = document.get_element_by_id("flag-btn").unwrap();
        flag_btn.add_event_listener_with_callback("click", flag_btn_handler.as_ref().unchecked_ref())?;

        flag_btn.remove_attribute("disabled")?;

        flag_btn_handler.forget();
    }
    Ok(())
}

fn send_password(key: KeyData) -> Box<Future<Item=JsValue, Error=JsValue>> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    let password_input = document.get_element_by_id("password-input").unwrap();
    let password_input = password_input.dyn_ref::<web_sys::HtmlInputElement>().unwrap();
    let password = password_input.value();

    let encrypted = encrypt(password.as_bytes(), &key.key);

    let req_body = json!( PasswordRequest { id: key.id.clone(),
                                            encrypted_password: base64::encode(&encrypted)} ).to_string();
    let mut opts = RequestInit::new();
    opts.method("POST");
    opts.body(Some(&JsValue::from_str(&req_body)));

    let request = Request::new_with_str_and_init(
        "./api/check-password",
        &opts,
    ).unwrap();

    request.headers().set("Content-Type", "application/json").unwrap();

    let request_promise = window.fetch_with_request(&request);

    let future = JsFuture::from(request_promise)
        .and_then(|resp_value| {
            let resp: Response = resp_value.dyn_into().unwrap();
            resp.json()
        })
        .and_then(|json_value: Promise| {
            // Convert this other `Promise` into a rust `Future`.
            JsFuture::from(json_value)
        })
        .and_then(move |json| {
            // Use serde to parse the JSON into a struct.
            let response_data: Data = json.into_serde().unwrap();
            let password_box = document.get_element_by_id("password-box").unwrap();
            password_box.set_inner_html(&response_data.data);
            future::ok(JsValue::null())
        });

    Box::new(future)
}

fn check_flag() -> Box<Future<Item=JsValue, Error=JsValue>>{
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    let flag_input = document.get_element_by_id("flag-input").unwrap();
    let flag_input = flag_input.dyn_ref::<web_sys::HtmlInputElement>().unwrap();
    let flag = flag_input.value();

    let req_body = json!( Data{ data: flag } ).to_string();

    let mut opts = RequestInit::new();
    opts.method("POST");
    opts.body(Some(&JsValue::from_str(&req_body)));

    let request = Request::new_with_str_and_init(
        "./api/verify",
        &opts,
    ).unwrap();

    request.headers().set("Content-Type", "application/json").unwrap();

    let request_promise = window.fetch_with_request(&request);

    let future = JsFuture::from(request_promise)
        .and_then(|resp_value| {
            let resp: Response = resp_value.dyn_into().unwrap();
            resp.json()
        })
        .and_then(|json_value: Promise| {
            // Convert this other `Promise` into a rust `Future`.
            JsFuture::from(json_value)
        })
        .and_then(move |json| {
            // Use serde to parse the JSON into a struct.
            let response_data: Data = json.into_serde().unwrap();
            let flag_box = document.get_element_by_id("flag-box").unwrap();
            flag_box.set_inner_html(&response_data.data);
            future::ok(JsValue::null())
        });

    Box::new(future)
}

fn encrypt(data: &[u8], key: &[u8]) -> Vec<u8> {
    let mut rng = OsRng::new().unwrap();
    let mut iv = [0u8; 16];
    rng.fill_bytes(&mut iv);

    let cipher = Cbc::<Aes256, Pkcs7>::new_var(key, &iv).unwrap();
    let mut encrypted = cipher.encrypt_vec(data);
    let mut result = Vec::from(&iv[0..16]);
    result.append(&mut encrypted);
    result
}
