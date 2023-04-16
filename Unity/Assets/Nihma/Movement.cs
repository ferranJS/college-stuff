using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement : MonoBehaviour
{
    public Animator animator;
    // Start is called before the first frame update
    public float v = 0.0f;
    public float h = 0.0f;

    public bool cameraOn = false;
    public GameObject camara;
    public Transform nihma;
    void Start()
    {
        animator = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        if(h>0.08 || h<-0.08){
            if(h>0) {
                h-=0.07f;
            }else if(h<=0){
                h+=0.07f;
            }
        }else h=0.0f;
           
        if(v>0) {
            v-=0.07f;
        }else if(v<0){
            v+=0.07f;
        }
         
        if(v<0) v=0;

        if (Input.GetKey(KeyCode.W)) {
            if(v<=1) {
                v+=0.16f;
            }
        }
        if(Input.GetKey(KeyCode.A)){
            if(h>-1) {
                h-=0.16f;
            }
        }
        if(Input.GetKey(KeyCode.D)){
            if(h<1) {
                h+=0.16f;
            }
        }
        if(Input.GetKey(KeyCode.S)){
        }
        animator.SetFloat("vertical", v);
        animator.SetFloat("horizontal", h);

        if(cameraOn) {
            // nihma.transform.position = new Vector3(-0.4f, 2.7f, -28.9f);
            // nihma.transform.rotation = new Quaternion(0f,1.0f,-0.1f,0.1f);
            nihma.transform.position = camara.transform.position;
            nihma.transform.rotation = camara.transform.rotation;
            camara.transform.SetParent(nihma);
        }
        cameraOn = false; 
    }
}


