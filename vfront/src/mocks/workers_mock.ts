import { Workers } from "@/models/Workers";

let id = 0;

export default {
  mock: new Workers([
    // test data for now
    {
      worker_id: String(id++),
      name: "Анастасия Ковалева",
      job_title: "Мастер-бровист",
      display_description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
      worker_id: String(id++),
      name: "Анастасия Ковалева",
      job_title: "Мастер-бровист",
      display_description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
      worker_id: String(id++),
      name: "Анастасия Ковалева",
      job_title: "Мастер-бровист",
      display_description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
      worker_id: String(id++),
      name: "Анастасия Ковалева",
      job_title: "Мастер-бровист",
      display_description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
      worker_id: String(id++),
      name: "Анастасия Ковалева",
      job_title: "Мастер-бровист",
      display_description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
      worker_id: String(id++),
      name: "Анастасия Ковалева",
      job_title: "Мастер-бровист",
      display_description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
  ]),
};
