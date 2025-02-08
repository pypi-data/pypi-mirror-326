use foxglove::schemas::{
    Color, CubePrimitive, FrameTransform, Pose, Quaternion, SceneEntity, SceneUpdate, Vector3,
};
use foxglove::static_typed_channel;
use schemars::JsonSchema;
use serde::Serialize;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;

fn euler_to_quaternion(roll: f64, pitch: f64, yaw: f64) -> Quaternion {
    let quat = quaternion::euler_angles(roll, pitch, yaw);
    Quaternion {
        x: quat.1[0],
        y: quat.1[1],
        z: quat.1[2],
        w: quat.0,
    }
}

#[derive(Debug, Serialize, JsonSchema)]
struct Message {
    msg: String,
    count: u32,
}

static_typed_channel!(pub BOX_CHANNEL, "/boxes", SceneUpdate);
static_typed_channel!(pub TF_CHANNEL, "/tf", FrameTransform);
static_typed_channel!(pub MSG_CHANNEL, "/msg", Message);

#[allow(dead_code)]
pub fn log_blocking(fps: u8, stop: Arc<AtomicBool>) {
    let mut counter: u32 = 0;
    let duration = Duration::from_millis(1000 / u64::from(fps));
    while !stop.load(Ordering::Relaxed) {
        log(counter);
        std::thread::sleep(duration);
        counter += 1;
    }
}

#[allow(dead_code)]
pub async fn log_forever(fps: u8) {
    let mut counter: u32 = 0;
    let mut interval = tokio::time::interval(Duration::from_millis(1000 / u64::from(fps)));
    loop {
        interval.tick().await;
        log(counter);
        counter += 1;
    }
}

pub fn log(counter: u32) {
    MSG_CHANNEL.log(&Message {
        msg: "Hello, world!".to_string(),
        count: counter,
    });

    BOX_CHANNEL.log(&SceneUpdate {
        deletions: vec![],
        entities: vec![SceneEntity {
            frame_id: "box".to_string(),
            id: "box_1".to_string(),
            lifetime: Some(prost_types::Duration {
                seconds: 10,
                nanos: 0,
            }),
            cubes: vec![CubePrimitive {
                pose: Some(Pose {
                    position: Some(Vector3 {
                        x: 0.0,
                        y: 0.0,
                        z: 3.0,
                    }),
                    orientation: Some(euler_to_quaternion(0.0, 0.0, f64::from(counter) * -0.1)),
                }),
                size: Some(Vector3 {
                    x: 1.0,
                    y: 1.0,
                    z: 1.0,
                }),
                color: Some(Color {
                    r: 1.0,
                    g: 0.0,
                    b: 0.0,
                    a: 1.0,
                }),
            }],
            ..Default::default()
        }],
    });

    TF_CHANNEL.log(&FrameTransform {
        parent_frame_id: "world".to_string(),
        child_frame_id: "box".to_string(),
        rotation: Some(euler_to_quaternion(1.0, 0.0, f64::from(counter) * 0.1)),
        ..Default::default()
    });
}
