const GUIDE = 2;
renderer.localClippingEnabled = true;
const unitMats = Object.values(M);          // only the AC unit is cut: the bedroom, the cup and the plant are never clipped
function setClip(p) { for (const m of unitMats) m.clippingPlanes = p.length ? p : null; }
// ---------- Post: tracing + downsampled accumulation ----------
const quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const quadGeo = new THREE.PlaneGeometry(2, 2);
const VQ = `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`;
const edgeMat = new THREE.ShaderMaterial({
  uniforms: { tC: { value: null }, tN: { value: null }, px: { value: new THREE.Vector2() }, rS: { value: 2.7 }, rO: { value: 1.7 }, rC: { value: 1.05 }, thD: { value: 0.0016 }, thO: { value: 0.012 }, thN: { value: 0.12 } },
  vertexShader: VQ,
  fragmentShader: `
  uniform sampler2D tC, tN; uniform vec2 px; uniform float rS, rO, rC, thD, thO, thN; varying vec2 vUv;
  float iz(vec4 s){ return s.a>0. ? 1./s.a : 0.; }
  void main(){
    vec4 c = texture2D(tC, vUv); vec4 n0 = texture2D(tN, vUv); float z0 = iz(n0); bool f0 = n0.a > 0.;
    float hf = abs(c.a - .5) < .2 ? 1. : 0.;
    float dS = 99.;
    for(int i=0;i<16;i++){
      float a = float(i)*0.392699; vec2 d = vec2(cos(a), sin(a));
      for(int k=1;k<=4;k++){ float r = float(k)*rS*0.3; vec2 o = vUv + d*px*r; vec4 s = texture2D(tN, o);
        if((s.a>0.) != f0){ dS = min(dS, r); }
        if(k<=2){ float ca = texture2D(tC, o).a; if(abs(ca - .5) < .2) hf = 1.; } }
    }
    float eS = hf > .5 ? 1. - smoothstep(rS*0.3, rS*0.62, dS) : 1. - smoothstep(rS*0.62, rS*1.12, dS);
    float eO = 0., eC = 0.;
    vec2 dirs[4]; dirs[0]=vec2(1.,0.); dirs[1]=vec2(0.,1.); dirs[2]=vec2(.7071,.7071); dirs[3]=vec2(.7071,-.7071);
    for(int i=0;i<4;i++){
      vec4 a = texture2D(tN, vUv + dirs[i]*px*rO), b = texture2D(tN, vUv - dirs[i]*px*rO);
      if(f0 && a.a>0. && b.a>0.){
        float za = iz(a), zb = iz(b), m = max(z0, max(za, zb));
        eO = max(eO, smoothstep(thO, thO*1.8, abs(za + zb - 2.*z0) / m));
      }
      vec4 a2 = texture2D(tN, vUv + dirs[i]*px*rC), b2 = texture2D(tN, vUv - dirs[i]*px*rC);
      if(f0 && a2.a>0. && b2.a>0.){
        float za = iz(a2), zb = iz(b2), m = max(z0, max(za, zb));
        eC = max(eC, smoothstep(thD, thD*2.2, abs(za + zb - 2.*z0) / m));
        eC = max(eC, smoothstep(thN, thN*1.8, 1.-dot(n0.xyz, a2.xyz)));
        eC = max(eC, smoothstep(thN, thN*1.8, 1.-dot(n0.xyz, b2.xyz)));
      }
    }
    vec3 inkS = vec3(.078), inkO = vec3(.11), inkC = vec3(.25);
    float wS = eS, wO = eO*.95, wC = eC*.78;
    if(hf > .5){ wO *= .8; wC *= .75; inkS = vec3(.30); inkO = vec3(.36); inkC = vec3(.52); }
    float e = max(wS, max(wO, wC));
    vec3 ink = wS >= max(wO, wC) ? inkS : (wO >= wC ? inkO : inkC);
    vec3 col = mix(c.rgb, ink, e);
    float al = max(c.a > .01 ? 1. : 0., e);
    gl_FragColor = vec4(col*al, al);
  }`, depthTest: false, depthWrite: false, blending: THREE.NoBlending });
const downMat = new THREE.ShaderMaterial({
  uniforms: { tE: { value: null }, px: { value: new THREE.Vector2() }, w: { value: 1 } },
  vertexShader: VQ,
  fragmentShader: `
  uniform sampler2D tE; uniform vec2 px; uniform float w; varying vec2 vUv;
  void main(){
    vec4 s = texture2D(tE, vUv + px*vec2(.5,.5)) + texture2D(tE, vUv + px*vec2(-.5,.5)) + texture2D(tE, vUv + px*vec2(.5,-.5)) + texture2D(tE, vUv + px*vec2(-.5,-.5));
    gl_FragColor = s*.25*w;
  }`, depthTest: false, depthWrite: false, transparent: true,
  blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor });
const copyMat = new THREE.ShaderMaterial({
  uniforms: { tA: { value: null }, circ: { value: new THREE.Vector3() }, size: { value: new THREE.Vector2() }, fadeA: { value: new THREE.Vector2() }, fadeB: { value: new THREE.Vector2() }, fadeOn: { value: 0 } }, vertexShader: VQ,
  fragmentShader: `uniform sampler2D tA; uniform vec3 circ; uniform vec2 size; uniform vec2 fadeA, fadeB; uniform float fadeOn; varying vec2 vUv;
  void main(){ vec4 s = texture2D(tA, vUv); s = vec4(min(s.rgb, vec3(s.a)), min(s.a, 1.));
    if(fadeOn > .5){ vec2 p = vec2(vUv.x, 1. - vUv.y)*size; vec2 ab = fadeB - fadeA; float u = dot(p - fadeA, ab) / dot(ab, ab); s *= 1. - smoothstep(0., 1., u); }
    if(circ.z > 0.){ float d = distance(vUv*size, circ.xy); if(d > circ.z) discard;
      vec3 paper = vec3(.965,.961,.941); gl_FragColor = vec4(s.rgb + paper*(1.-s.a), 1.); return; }
    gl_FragColor = s; }`,
  depthTest: false, depthWrite: false, blending: THREE.NoBlending });
const quad = new THREE.Mesh(quadGeo, edgeMat); const quadScene = new THREE.Scene(); quadScene.add(quad);
const RT = {};
function targets(key, w, h) {
  if (RT[key]) return RT[key];
  const lin = { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter };
  RT[key] = {
    c: new THREE.WebGLRenderTarget(w * SS, h * SS, { type: THREE.UnsignedByteType, ...lin }),
    n: new THREE.WebGLRenderTarget(w * SS, h * SS, { type: THREE.FloatType, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter }),
    e: new THREE.WebGLRenderTarget(w * SS, h * SS, { type: THREE.UnsignedByteType, ...lin }),
    a: new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, ...lin }),
  };
  return RT[key];
}
function pass(t, cam, opt, wgt) {
  setClip(opt.clip || []);
  U.uMode.value = 1; cam.layers.set(0);
  scene.traverse(o => { if (o.userData.noND) o.visible = false; });
  renderer.setRenderTarget(t.n); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, cam);
  scene.traverse(o => { if (o.userData.noND) o.visible = true; });
  U.uMode.value = 0; cam.layers.set(0); if (opt.guides) cam.layers.enable(GUIDE);
  renderer.setRenderTarget(t.c); renderer.setClearColor(0xffffff, 0); renderer.clear(); renderer.render(scene, cam);
  setClip([]);
  quad.material = edgeMat; edgeMat.uniforms.tC.value = t.c.texture; edgeMat.uniforms.tN.value = t.n.texture;
  edgeMat.uniforms.px.value.set(1 / t.c.width, 1 / t.c.height);
  renderer.setRenderTarget(t.e); renderer.clear(); renderer.render(quadScene, quadCam);
  quad.material = downMat; downMat.uniforms.tE.value = t.e.texture; downMat.uniforms.px.value.set(1 / t.e.width, 1 / t.e.height); downMat.uniforms.w.value = wgt;
  renderer.setRenderTarget(t.a); renderer.render(quadScene, quadCam);
}
const JOFF = [[-0.125, -0.375], [0.375, -0.125], [0.125, 0.375], [-0.375, 0.125], [0, 0], [0.25, 0.25], [-0.25, 0.25], [0.25, -0.25]];
const SHUTTER = 0.12 / 24;
// rect: screen pixels (origin top left); setup(dt, jitter) poses the scene and returns the camera
function renderView(key, rect, setup, opt = {}) {
  const t = targets(`${key}-${rect.w}x${rect.h}`, rect.w, rect.h);     // targets cached by size: as the magnifier grows it can't reuse a smaller target
  renderer.setRenderTarget(t.a); renderer.setClearColor(0x000000, 0); renderer.clear();
  for (let k = 0; k < JIT; k++) {
    const dt = JIT > 1 ? (k / (JIT - 1) - 0.5) * SHUTTER : 0;
    const r = setup(dt, JOFF[k % JOFF.length]);
    pass(t, r.cam, { ...opt, clip: r.clip || [] }, 1 / JIT);
  }
  quad.material = copyMat; copyMat.uniforms.tA.value = t.a.texture;
  copyMat.uniforms.fadeOn.value = 0;
  copyMat.uniforms.size.value.set(rect.w, rect.h); copyMat.uniforms.circ.value.set(rect.w / 2, rect.h / 2, opt.circle ? rect.w / 2 : 0);
  renderer.setRenderTarget(null); renderer.setViewport(rect.x, PY - rect.y - rect.h, rect.w, rect.h); renderer.setScissor(rect.x, PY - rect.y - rect.h, rect.w, rect.h); renderer.setScissorTest(true);
  renderer.render(quadScene, quadCam); renderer.setScissorTest(false); renderer.setViewport(0, 0, PX, PY);
}

