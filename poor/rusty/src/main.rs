use std::sync::{Arc, Mutex};

// use std::thread;
use std::any::Any;
use std::fmt;

trait Observer {
    fn notify(&self, sender: &Observable, event: Box<dyn Any + Send>);
}

struct Observable {
    name: String,
    observers: Vec<Arc<Mutex<dyn Observer + Send>>>,
    event_queue: Arc<Mutex<Vec<(String, Box<dyn Any + Send>)>>>,
    #[allow(dead_code)]
    please_shutdown: Arc<Mutex<bool>>,
}

impl Observable {
    fn new(name: &str) -> Arc<Mutex<Self>> {
        let observable = Observable {
            name: name.to_string(),
            observers: Vec::new(),
            event_queue: Arc::new(Mutex::new(Vec::new())),
            please_shutdown: Arc::new(Mutex::new(false)),
        };
        Arc::new(Mutex::new(observable))
    }

    // mark as may be unused:
    #[allow(dead_code)]
    fn new1(name: &str) -> Self {
        Observable {
            name: name.to_string(),
            observers: Vec::new(),
            #[allow(dead_code)]
            event_queue: Arc::new(Mutex::new(Vec::new())),
            #[allow(dead_code)]
            please_shutdown: Arc::new(Mutex::new(false)),
        }
    }
}


impl fmt::Debug for Observable {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Observable")
            .field("name", &self.name)
            .field("observer_count", &self.observers.len())
            .field("event_queue_length", &self.event_queue.lock().unwrap().len())
            .finish()
    }
}


fn main() {
    let z = Observable::new("z");
    let z2 = z.clone();
    // check how many instances of z are there:
    let instances = Arc::strong_count(&z);
    println!("there are {instances} instances of z.");
    println!("z: {:?}", z2);

    z2.lock().unwrap().name = "newZ3Name".to_string();
    println!("z2: {:?}", z2);
    println!("Hello, world!");
}
