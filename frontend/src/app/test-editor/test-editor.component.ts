import { Component, OnInit } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-test-editor',
  templateUrl: './test-editor.component.html',
  styleUrls: ['./test-editor.component.css'],
})
export class TestEditorComponent implements OnInit {
  ckeditorContent = this.reverse(
    `<p>уц ац цуау цуа уц wef e<img alt='' src='http://localhost:8000/post/photo/qxyzxrtz_%D0%91%D0%B0%D0%B7%D0%B0%D0%94%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.png' style='width:567px' /></p>`
  );
  image: any;
  constructor() {}

  ngOnInit(): void {}
  fileChange(event: any) {
    let fileList: FileList = event.target.files;
    if (!fileList.length) {
      return;
    }
    this.image = fileList[0];
  }
  convert(str: string) {
    str = str.replace(/"/g, "'");
    console.log(str);
    return str;
  }
  reverse(str: string) {
    str = str.replace(/'/g, `"`);
    console.log(str);
    return str;
  }
  display() {
    console.log(this.convert(this.ckeditorContent));
  }
  async unload() {
    let formData: FormData = new FormData();
    formData.append('file', this.image);

    return axios.post(`http://localhost:8000/post/upload_image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization:
          'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTczODg3NTMsImlhdCI6MTY1NzM4Njk1Mywic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJhYmVvYnZqOXlvb2EifQ.YzylLzgJLLRltBXy5Su7E-R_BVMi27RqXYk0eBKREnY',
        accept: 'application/json',
      },
    });
  }
}
