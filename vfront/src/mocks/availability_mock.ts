import { ClientAvailability } from "@/models/availability/ClientAvailability";

export default {
  mock: new ClientAvailability([
    {
      worker_id: 1,
      days: [
        {
          date: "2022-02-21",
          timeslots: [
            {
              dt_from: "2022-02-21T13:15:00",
              dt_to: "2022-02-21T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T15:00:00",
              dt_to: "2022-02-21T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T15:45:00",
              dt_to: "2022-02-21T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T16:30:00",
              dt_to: "2022-02-21T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T17:15:00",
              dt_to: "2022-02-21T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T18:00:00",
              dt_to: "2022-02-21T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T18:45:00",
              dt_to: "2022-02-21T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T19:30:00",
              dt_to: "2022-02-21T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T20:15:00",
              dt_to: "2022-02-21T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T21:00:00",
              dt_to: "2022-02-21T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T21:45:00",
              dt_to: "2022-02-21T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-02-28",
          timeslots: [
            {
              dt_from: "2022-02-28T13:15:00",
              dt_to: "2022-02-28T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T15:00:00",
              dt_to: "2022-02-28T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T15:45:00",
              dt_to: "2022-02-28T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T16:30:00",
              dt_to: "2022-02-28T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T17:15:00",
              dt_to: "2022-02-28T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T18:00:00",
              dt_to: "2022-02-28T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T18:45:00",
              dt_to: "2022-02-28T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T19:30:00",
              dt_to: "2022-02-28T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T20:15:00",
              dt_to: "2022-02-28T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T21:00:00",
              dt_to: "2022-02-28T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T21:45:00",
              dt_to: "2022-02-28T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-07",
          timeslots: [
            {
              dt_from: "2022-03-07T13:15:00",
              dt_to: "2022-03-07T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T15:00:00",
              dt_to: "2022-03-07T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T15:45:00",
              dt_to: "2022-03-07T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T16:30:00",
              dt_to: "2022-03-07T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T17:15:00",
              dt_to: "2022-03-07T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T18:00:00",
              dt_to: "2022-03-07T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T18:45:00",
              dt_to: "2022-03-07T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T19:30:00",
              dt_to: "2022-03-07T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T20:15:00",
              dt_to: "2022-03-07T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T21:00:00",
              dt_to: "2022-03-07T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T21:45:00",
              dt_to: "2022-03-07T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-14",
          timeslots: [
            {
              dt_from: "2022-03-14T13:15:00",
              dt_to: "2022-03-14T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T15:00:00",
              dt_to: "2022-03-14T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T15:45:00",
              dt_to: "2022-03-14T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T16:30:00",
              dt_to: "2022-03-14T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T17:15:00",
              dt_to: "2022-03-14T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T18:00:00",
              dt_to: "2022-03-14T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T18:45:00",
              dt_to: "2022-03-14T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T19:30:00",
              dt_to: "2022-03-14T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T20:15:00",
              dt_to: "2022-03-14T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T21:00:00",
              dt_to: "2022-03-14T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T21:45:00",
              dt_to: "2022-03-14T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-21",
          timeslots: [
            {
              dt_from: "2022-03-21T13:15:00",
              dt_to: "2022-03-21T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T15:00:00",
              dt_to: "2022-03-21T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T15:45:00",
              dt_to: "2022-03-21T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T16:30:00",
              dt_to: "2022-03-21T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T17:15:00",
              dt_to: "2022-03-21T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T18:00:00",
              dt_to: "2022-03-21T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T18:45:00",
              dt_to: "2022-03-21T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T19:30:00",
              dt_to: "2022-03-21T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T20:15:00",
              dt_to: "2022-03-21T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T21:00:00",
              dt_to: "2022-03-21T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T21:45:00",
              dt_to: "2022-03-21T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-28",
          timeslots: [
            {
              dt_from: "2022-03-28T13:15:00",
              dt_to: "2022-03-28T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T15:00:00",
              dt_to: "2022-03-28T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T15:45:00",
              dt_to: "2022-03-28T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T16:30:00",
              dt_to: "2022-03-28T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T17:15:00",
              dt_to: "2022-03-28T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T18:00:00",
              dt_to: "2022-03-28T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T18:45:00",
              dt_to: "2022-03-28T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T19:30:00",
              dt_to: "2022-03-28T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T20:15:00",
              dt_to: "2022-03-28T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T21:00:00",
              dt_to: "2022-03-28T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T21:45:00",
              dt_to: "2022-03-28T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-04",
          timeslots: [
            {
              dt_from: "2022-04-04T13:15:00",
              dt_to: "2022-04-04T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T15:00:00",
              dt_to: "2022-04-04T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T15:45:00",
              dt_to: "2022-04-04T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T16:30:00",
              dt_to: "2022-04-04T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T17:15:00",
              dt_to: "2022-04-04T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T18:00:00",
              dt_to: "2022-04-04T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T18:45:00",
              dt_to: "2022-04-04T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T19:30:00",
              dt_to: "2022-04-04T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T20:15:00",
              dt_to: "2022-04-04T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T21:00:00",
              dt_to: "2022-04-04T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T21:45:00",
              dt_to: "2022-04-04T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-11",
          timeslots: [
            {
              dt_from: "2022-04-11T13:15:00",
              dt_to: "2022-04-11T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T15:00:00",
              dt_to: "2022-04-11T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T15:45:00",
              dt_to: "2022-04-11T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T16:30:00",
              dt_to: "2022-04-11T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T17:15:00",
              dt_to: "2022-04-11T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T18:00:00",
              dt_to: "2022-04-11T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T18:45:00",
              dt_to: "2022-04-11T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T19:30:00",
              dt_to: "2022-04-11T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T20:15:00",
              dt_to: "2022-04-11T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T21:00:00",
              dt_to: "2022-04-11T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T21:45:00",
              dt_to: "2022-04-11T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-18",
          timeslots: [
            {
              dt_from: "2022-04-18T13:15:00",
              dt_to: "2022-04-18T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T15:00:00",
              dt_to: "2022-04-18T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T15:45:00",
              dt_to: "2022-04-18T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T16:30:00",
              dt_to: "2022-04-18T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T17:15:00",
              dt_to: "2022-04-18T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T18:00:00",
              dt_to: "2022-04-18T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T18:45:00",
              dt_to: "2022-04-18T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T19:30:00",
              dt_to: "2022-04-18T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T20:15:00",
              dt_to: "2022-04-18T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T21:00:00",
              dt_to: "2022-04-18T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T21:45:00",
              dt_to: "2022-04-18T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-25",
          timeslots: [
            {
              dt_from: "2022-04-25T13:15:00",
              dt_to: "2022-04-25T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T15:00:00",
              dt_to: "2022-04-25T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T15:45:00",
              dt_to: "2022-04-25T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T16:30:00",
              dt_to: "2022-04-25T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T17:15:00",
              dt_to: "2022-04-25T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T18:00:00",
              dt_to: "2022-04-25T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T18:45:00",
              dt_to: "2022-04-25T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T19:30:00",
              dt_to: "2022-04-25T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T20:15:00",
              dt_to: "2022-04-25T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T21:00:00",
              dt_to: "2022-04-25T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T21:45:00",
              dt_to: "2022-04-25T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-02",
          timeslots: [
            {
              dt_from: "2022-05-02T13:15:00",
              dt_to: "2022-05-02T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T15:00:00",
              dt_to: "2022-05-02T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T15:45:00",
              dt_to: "2022-05-02T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T16:30:00",
              dt_to: "2022-05-02T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T17:15:00",
              dt_to: "2022-05-02T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T18:00:00",
              dt_to: "2022-05-02T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T18:45:00",
              dt_to: "2022-05-02T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T19:30:00",
              dt_to: "2022-05-02T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T20:15:00",
              dt_to: "2022-05-02T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T21:00:00",
              dt_to: "2022-05-02T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T21:45:00",
              dt_to: "2022-05-02T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-09",
          timeslots: [
            {
              dt_from: "2022-05-09T13:15:00",
              dt_to: "2022-05-09T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T15:00:00",
              dt_to: "2022-05-09T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T15:45:00",
              dt_to: "2022-05-09T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T16:30:00",
              dt_to: "2022-05-09T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T17:15:00",
              dt_to: "2022-05-09T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T18:00:00",
              dt_to: "2022-05-09T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T18:45:00",
              dt_to: "2022-05-09T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T19:30:00",
              dt_to: "2022-05-09T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T20:15:00",
              dt_to: "2022-05-09T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T21:00:00",
              dt_to: "2022-05-09T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T21:45:00",
              dt_to: "2022-05-09T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-16",
          timeslots: [
            {
              dt_from: "2022-05-16T13:15:00",
              dt_to: "2022-05-16T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T15:00:00",
              dt_to: "2022-05-16T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T15:45:00",
              dt_to: "2022-05-16T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T16:30:00",
              dt_to: "2022-05-16T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T17:15:00",
              dt_to: "2022-05-16T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T18:00:00",
              dt_to: "2022-05-16T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T18:45:00",
              dt_to: "2022-05-16T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T19:30:00",
              dt_to: "2022-05-16T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T20:15:00",
              dt_to: "2022-05-16T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T21:00:00",
              dt_to: "2022-05-16T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T21:45:00",
              dt_to: "2022-05-16T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-23",
          timeslots: [
            {
              dt_from: "2022-05-23T13:15:00",
              dt_to: "2022-05-23T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T15:00:00",
              dt_to: "2022-05-23T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T15:45:00",
              dt_to: "2022-05-23T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T16:30:00",
              dt_to: "2022-05-23T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T17:15:00",
              dt_to: "2022-05-23T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T18:00:00",
              dt_to: "2022-05-23T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T18:45:00",
              dt_to: "2022-05-23T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T19:30:00",
              dt_to: "2022-05-23T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T20:15:00",
              dt_to: "2022-05-23T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T21:00:00",
              dt_to: "2022-05-23T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T21:45:00",
              dt_to: "2022-05-23T22:30:00",
              slot_type: "available",
            },
          ],
        },
      ],
    },
    {
      worker_id: 2,
      days: [
        {
          date: "2022-02-21",
          timeslots: [
            {
              dt_from: "2022-02-21T13:15:00",
              dt_to: "2022-02-21T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T15:00:00",
              dt_to: "2022-02-21T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T15:45:00",
              dt_to: "2022-02-21T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T16:30:00",
              dt_to: "2022-02-21T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T17:15:00",
              dt_to: "2022-02-21T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T18:00:00",
              dt_to: "2022-02-21T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T18:45:00",
              dt_to: "2022-02-21T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T19:30:00",
              dt_to: "2022-02-21T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T20:15:00",
              dt_to: "2022-02-21T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T21:00:00",
              dt_to: "2022-02-21T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-21T21:45:00",
              dt_to: "2022-02-21T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-02-28",
          timeslots: [
            {
              dt_from: "2022-02-28T13:15:00",
              dt_to: "2022-02-28T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T15:00:00",
              dt_to: "2022-02-28T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T15:45:00",
              dt_to: "2022-02-28T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T16:30:00",
              dt_to: "2022-02-28T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T17:15:00",
              dt_to: "2022-02-28T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T18:00:00",
              dt_to: "2022-02-28T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T18:45:00",
              dt_to: "2022-02-28T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T19:30:00",
              dt_to: "2022-02-28T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T20:15:00",
              dt_to: "2022-02-28T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T21:00:00",
              dt_to: "2022-02-28T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-02-28T21:45:00",
              dt_to: "2022-02-28T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-07",
          timeslots: [
            {
              dt_from: "2022-03-07T13:15:00",
              dt_to: "2022-03-07T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T15:00:00",
              dt_to: "2022-03-07T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T15:45:00",
              dt_to: "2022-03-07T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T16:30:00",
              dt_to: "2022-03-07T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T17:15:00",
              dt_to: "2022-03-07T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T18:00:00",
              dt_to: "2022-03-07T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T18:45:00",
              dt_to: "2022-03-07T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T19:30:00",
              dt_to: "2022-03-07T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T20:15:00",
              dt_to: "2022-03-07T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T21:00:00",
              dt_to: "2022-03-07T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-07T21:45:00",
              dt_to: "2022-03-07T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-14",
          timeslots: [
            {
              dt_from: "2022-03-14T13:15:00",
              dt_to: "2022-03-14T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T15:00:00",
              dt_to: "2022-03-14T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T15:45:00",
              dt_to: "2022-03-14T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T16:30:00",
              dt_to: "2022-03-14T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T17:15:00",
              dt_to: "2022-03-14T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T18:00:00",
              dt_to: "2022-03-14T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T18:45:00",
              dt_to: "2022-03-14T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T19:30:00",
              dt_to: "2022-03-14T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T20:15:00",
              dt_to: "2022-03-14T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T21:00:00",
              dt_to: "2022-03-14T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-14T21:45:00",
              dt_to: "2022-03-14T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-21",
          timeslots: [
            {
              dt_from: "2022-03-21T13:15:00",
              dt_to: "2022-03-21T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T15:00:00",
              dt_to: "2022-03-21T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T15:45:00",
              dt_to: "2022-03-21T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T16:30:00",
              dt_to: "2022-03-21T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T17:15:00",
              dt_to: "2022-03-21T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T18:00:00",
              dt_to: "2022-03-21T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T18:45:00",
              dt_to: "2022-03-21T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T19:30:00",
              dt_to: "2022-03-21T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T20:15:00",
              dt_to: "2022-03-21T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T21:00:00",
              dt_to: "2022-03-21T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-21T21:45:00",
              dt_to: "2022-03-21T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-03-28",
          timeslots: [
            {
              dt_from: "2022-03-28T13:15:00",
              dt_to: "2022-03-28T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T15:00:00",
              dt_to: "2022-03-28T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T15:45:00",
              dt_to: "2022-03-28T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T16:30:00",
              dt_to: "2022-03-28T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T17:15:00",
              dt_to: "2022-03-28T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T18:00:00",
              dt_to: "2022-03-28T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T18:45:00",
              dt_to: "2022-03-28T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T19:30:00",
              dt_to: "2022-03-28T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T20:15:00",
              dt_to: "2022-03-28T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T21:00:00",
              dt_to: "2022-03-28T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-03-28T21:45:00",
              dt_to: "2022-03-28T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-04",
          timeslots: [
            {
              dt_from: "2022-04-04T13:15:00",
              dt_to: "2022-04-04T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T15:00:00",
              dt_to: "2022-04-04T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T15:45:00",
              dt_to: "2022-04-04T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T16:30:00",
              dt_to: "2022-04-04T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T17:15:00",
              dt_to: "2022-04-04T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T18:00:00",
              dt_to: "2022-04-04T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T18:45:00",
              dt_to: "2022-04-04T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T19:30:00",
              dt_to: "2022-04-04T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T20:15:00",
              dt_to: "2022-04-04T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T21:00:00",
              dt_to: "2022-04-04T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-04T21:45:00",
              dt_to: "2022-04-04T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-11",
          timeslots: [
            {
              dt_from: "2022-04-11T13:15:00",
              dt_to: "2022-04-11T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T15:00:00",
              dt_to: "2022-04-11T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T15:45:00",
              dt_to: "2022-04-11T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T16:30:00",
              dt_to: "2022-04-11T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T17:15:00",
              dt_to: "2022-04-11T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T18:00:00",
              dt_to: "2022-04-11T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T18:45:00",
              dt_to: "2022-04-11T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T19:30:00",
              dt_to: "2022-04-11T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T20:15:00",
              dt_to: "2022-04-11T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T21:00:00",
              dt_to: "2022-04-11T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-11T21:45:00",
              dt_to: "2022-04-11T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-18",
          timeslots: [
            {
              dt_from: "2022-04-18T13:15:00",
              dt_to: "2022-04-18T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T15:00:00",
              dt_to: "2022-04-18T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T15:45:00",
              dt_to: "2022-04-18T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T16:30:00",
              dt_to: "2022-04-18T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T17:15:00",
              dt_to: "2022-04-18T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T18:00:00",
              dt_to: "2022-04-18T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T18:45:00",
              dt_to: "2022-04-18T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T19:30:00",
              dt_to: "2022-04-18T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T20:15:00",
              dt_to: "2022-04-18T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T21:00:00",
              dt_to: "2022-04-18T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-18T21:45:00",
              dt_to: "2022-04-18T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-04-25",
          timeslots: [
            {
              dt_from: "2022-04-25T13:15:00",
              dt_to: "2022-04-25T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T15:00:00",
              dt_to: "2022-04-25T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T15:45:00",
              dt_to: "2022-04-25T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T16:30:00",
              dt_to: "2022-04-25T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T17:15:00",
              dt_to: "2022-04-25T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T18:00:00",
              dt_to: "2022-04-25T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T18:45:00",
              dt_to: "2022-04-25T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T19:30:00",
              dt_to: "2022-04-25T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T20:15:00",
              dt_to: "2022-04-25T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T21:00:00",
              dt_to: "2022-04-25T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-04-25T21:45:00",
              dt_to: "2022-04-25T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-02",
          timeslots: [
            {
              dt_from: "2022-05-02T13:15:00",
              dt_to: "2022-05-02T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T15:00:00",
              dt_to: "2022-05-02T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T15:45:00",
              dt_to: "2022-05-02T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T16:30:00",
              dt_to: "2022-05-02T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T17:15:00",
              dt_to: "2022-05-02T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T18:00:00",
              dt_to: "2022-05-02T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T18:45:00",
              dt_to: "2022-05-02T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T19:30:00",
              dt_to: "2022-05-02T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T20:15:00",
              dt_to: "2022-05-02T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T21:00:00",
              dt_to: "2022-05-02T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-02T21:45:00",
              dt_to: "2022-05-02T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-09",
          timeslots: [
            {
              dt_from: "2022-05-09T13:15:00",
              dt_to: "2022-05-09T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T15:00:00",
              dt_to: "2022-05-09T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T15:45:00",
              dt_to: "2022-05-09T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T16:30:00",
              dt_to: "2022-05-09T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T17:15:00",
              dt_to: "2022-05-09T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T18:00:00",
              dt_to: "2022-05-09T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T18:45:00",
              dt_to: "2022-05-09T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T19:30:00",
              dt_to: "2022-05-09T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T20:15:00",
              dt_to: "2022-05-09T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T21:00:00",
              dt_to: "2022-05-09T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-09T21:45:00",
              dt_to: "2022-05-09T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-16",
          timeslots: [
            {
              dt_from: "2022-05-16T13:15:00",
              dt_to: "2022-05-16T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T15:00:00",
              dt_to: "2022-05-16T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T15:45:00",
              dt_to: "2022-05-16T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T16:30:00",
              dt_to: "2022-05-16T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T17:15:00",
              dt_to: "2022-05-16T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T18:00:00",
              dt_to: "2022-05-16T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T18:45:00",
              dt_to: "2022-05-16T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T19:30:00",
              dt_to: "2022-05-16T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T20:15:00",
              dt_to: "2022-05-16T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T21:00:00",
              dt_to: "2022-05-16T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-16T21:45:00",
              dt_to: "2022-05-16T22:30:00",
              slot_type: "available",
            },
          ],
        },
        {
          date: "2022-05-23",
          timeslots: [
            {
              dt_from: "2022-05-23T13:15:00",
              dt_to: "2022-05-23T14:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T15:00:00",
              dt_to: "2022-05-23T15:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T15:45:00",
              dt_to: "2022-05-23T16:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T16:30:00",
              dt_to: "2022-05-23T17:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T17:15:00",
              dt_to: "2022-05-23T18:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T18:00:00",
              dt_to: "2022-05-23T18:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T18:45:00",
              dt_to: "2022-05-23T19:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T19:30:00",
              dt_to: "2022-05-23T20:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T20:15:00",
              dt_to: "2022-05-23T21:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T21:00:00",
              dt_to: "2022-05-23T21:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-05-23T21:45:00",
              dt_to: "2022-05-23T22:30:00",
              slot_type: "available",
            },
          ],
        },
      ],
    },
    {
      worker_id: 3,
      days: [
        {
          date: "2022-01-01",
          timeslots: [
            {
              dt_from: "2022-01-01T08:00:00",
              dt_to: "2022-01-01T08:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T10:00:00",
              dt_to: "2022-01-01T10:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T10:45:00",
              dt_to: "2022-01-01T11:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T11:30:00",
              dt_to: "2022-01-01T12:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T12:15:00",
              dt_to: "2022-01-01T13:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T13:00:00",
              dt_to: "2022-01-01T13:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T13:45:00",
              dt_to: "2022-01-01T14:30:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T14:30:00",
              dt_to: "2022-01-01T15:15:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T15:15:00",
              dt_to: "2022-01-01T16:00:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T16:00:00",
              dt_to: "2022-01-01T16:45:00",
              slot_type: "available",
            },
            {
              dt_from: "2022-01-01T16:45:00",
              dt_to: "2022-01-01T17:30:00",
              slot_type: "available",
            },
          ],
        },
      ],
    },
  ]),
};
