using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShakeCamera : MonoBehaviour
{
    // Start is called before the first frame update
    public bool shaking = true;
    public float duration = 1.0f;
    public float power = 0.7f;
    public float slowDownAmount = 1.0f;

    public Transform camera;

    Vector3 startPosition;
    float initialDuration;

    void Start()
    {
        camera = Camera.main.transform;
        startPosition = camera.localPosition;
        initialDuration = duration;
    }

    // Update is called once per frame
    void Update()
    {
        if(shaking){
            if(duration >0) {
                camera.localPosition = startPosition + Random.insideUnitSphere * power;
                duration -= Time.deltaTime * slowDownAmount;
            }
            else{
                shaking = false;
                duration = initialDuration;
                camera.localPosition = startPosition;
            }
        }
    }
}
