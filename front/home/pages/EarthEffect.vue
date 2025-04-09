<template>
  <div ref="earthContainer" class="earth-container"></div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import * as THREE from "three";

const earthContainer = ref(null);

onMounted(() => {
  // ✅ Scene, Camera, Renderer 설정
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

  const width = earthContainer.value.clientWidth || 400;
  const height = earthContainer.value.clientHeight || 400;
  renderer.setSize(width, height);
  earthContainer.value.appendChild(renderer.domElement);

  // ✅ 텍스처 로드 (🚨 `public/` 경로 사용)
  const textureLoader = new THREE.TextureLoader();
  const earthTexture = textureLoader.load("/textures/8k_earth_daymap.jpg", (texture) => {
      texture.anisotropy = renderer.capabilities.getMaxAnisotropy(); // ✅ 텍스처 선명하게
  });
  const cloudsTexture = textureLoader.load("/textures/8k_earth_clouds.jpg", (texture) => {
      texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
  });
  const nightTexture = textureLoader.load("/textures/8k_earth_nightmap.jpg", (texture) => {
      texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
  });
  const specularTexture = textureLoader.load("/textures/8k_earth_specular.jpg"); // ✅ 반사 텍스처 추가

  // ✅ 지구본 만들기
  const earthGeometry = new THREE.SphereGeometry(1, 64, 64);
  const earthMaterial = new THREE.MeshStandardMaterial({
      map: earthTexture,
      emissiveMap: nightTexture,
      emissiveIntensity: 5, // ✅ 야간 조명 더 밝게
      roughness: 0.5, // ✅ 반사 효과 추가
      metalness: 0.3, // ✅ 표면 반사도 추가
  });
  const earth = new THREE.Mesh(earthGeometry, earthMaterial);
  scene.add(earth);

  // ✅ 구름 레이어 추가
  const cloudGeometry = new THREE.SphereGeometry(1.02, 64, 64);
  const cloudMaterial = new THREE.MeshStandardMaterial({
      map: cloudsTexture,
      transparent: true,
      opacity: 0.5,
  });
  const clouds = new THREE.Mesh(cloudGeometry, cloudMaterial);
  scene.add(clouds);

  // ✅ 조명 추가 (🚀 더 밝게 조절)
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.0);
  const directionalLight = new THREE.DirectionalLight(0xffffff, 3);
  directionalLight.position.set(5, 3, 5);
  scene.add(ambientLight, directionalLight);

  // ✅ 카메라 위치 조정
  camera.position.z = 3.5;

  // ✅ 애니메이션 (지구 회전)
  const animate = () => {
    requestAnimationFrame(animate);
    earth.rotation.y += 0.002;
    clouds.rotation.y += 0.003;
    renderer.render(scene, camera);
  };

  animate();

  // ✅ 마우스 이벤트 (확대 효과)
  earthContainer.value.addEventListener("mousemove", (event) => {
    const { clientX, clientY } = event;
    const { width, height } = earthContainer.value.getBoundingClientRect();

    const x = (clientX / width) * 2 - 2;
    const y = -(clientY / height) * 2 + 2;

    camera.position.x = x * 0.5;
    camera.position.y = y * 0.5;
    camera.lookAt(earth.position);
  });

  // ✅ 마우스 나가면 원래 위치로 복귀
  earthContainer.value.addEventListener("mouseleave", () => {
    camera.position.set(0, 0, 3.5);
    camera.lookAt(earth.position);
  });
});
</script>

<style scoped>
.earth-container {
  width: 400px;
  height: 400px;
  margin: 0 auto;
  position: absolute;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
}
</style>
