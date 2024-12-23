import { Component, AfterViewInit } from '@angular/core';
import { ImageService } from '../Service/image.service';

@Component({
  selector: 'app-cam',
  templateUrl: './cam.component.html',
  styleUrls: ['./cam.component.scss'] 
})
export class CamComponent implements AfterViewInit {
  videoElement!: HTMLVideoElement;
  canvasElement!: HTMLCanvasElement;
  result: String | null = null;

  constructor(private imageService: ImageService) {}

  ngAfterViewInit() {
    this.videoElement = document.getElementById('video') as HTMLVideoElement;
    this.canvasElement = document.getElementById('canvas') as HTMLCanvasElement;

    // Truy cập camera
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        this.videoElement.srcObject = stream;
      })
      .catch((error) => {
        console.error("Không thể truy cập camera: ", error);
      });
  }

  capture() {
    const context = this.canvasElement.getContext('2d');
    if (context) {
      context.drawImage(this.videoElement, 0, 0, this.canvasElement.width, this.canvasElement.height);
      
      // Lấy dữ liệu ảnh từ canvas
      this.canvasElement.toBlob((blob) => {
        if (blob) {
          const formData = new FormData();
          // Đính kèm blob như là file ảnh
          formData.append('image', blob, 'captured_image.jpg');
  
          // Gửi request đến back-end
          this.imageService.getLabel(formData).subscribe({
            next: (response: any) => {
              console.log('Response:', response);                           
              this.result = response.fruit;
            }, 
            error: (error: any) => {
              console.error('Error:', error);
            }
          });
        }
      }, 'image/jpeg');  // Tạo blob dưới dạng JPEG
    }
  }
  
}
